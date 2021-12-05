from flask import (
    render_template,
    redirect,
    url_for,
    request,
    flash,
    current_app,
    abort,
)
from logging import getLogger
from . import content_bp
from ..models import db_session_manager, Post, db, Role
from flask_login import current_user
from flask_login import login_required
from .forms import (
    PostForm,
    PostUpdateForm,
    PostCommentForm
)
from sqlalchemy.orm import aliased

logger = getLogger(__name__)


@content_bp.get("/blog_posts")
@content_bp.post("/blog_posts")
def blog_posts():
    """This function dispatches control to the correct handler
    based on the URL and the query string

    Returns:
        Response: The Flask Response object with the rendered page
    """
    if request.args.get("action") is None:
        return blog_posts_display()
    elif request.args.get("action") == "create":
        return blog_post_create()
    else:
        abort(404)


def blog_posts_display():
    """Content home page, presents a list of blog posts (abbreviated)
    to the user that are clickable for the full post page

    Returns:
        text: the rendered HTML for the page
    """
    logger.debug("rendering blog posts page")
    search = request.args.get("search")
    with db_session_manager() as db_session:
        page = request.args.get("page", type=int)
        posts = (
            db_session
            .query(Post)
            .filter(Post.parent_uid is None)
            .order_by(Post.updated.desc())
        )
        # can the current user view only active posts:
        if current_user.is_anonymous or current_user.can_view_posts():
            posts = posts.filter(Post.active == True)

        # is the user searching for content in the posts?
        if search is not None:
            posts = posts.filter(Post.content.like(f"%{search}%"))
        posts = (
            posts.paginate(
                page=page,
                per_page=current_app.config["BLOG_POSTS_PER_PAGE"],
                error_out=False
            )
        )
    return render_template("posts.html", posts=posts)


@login_required
def blog_post_create():
    """Provides a page where blog post content can be created

    Returns:
        text: the rendered HTML for the page
    """
    logger.debug("rendering blog post edit create page")
    form = PostForm()
    if form.cancel.data:
        return redirect(url_for("intro_bp.home"))
    if form.validate_on_submit():
        with db_session_manager() as db_session:
            post = Post(
                user_uid=current_user.user_uid,
                title=form.title.data.strip(),
                content=form.content.data.strip(),
            )
            db_session.add(post)
            db_session.commit()
            flash(f"Blog post '{form.title.data.strip()}' created")
            return redirect(url_for("content_bp.blog_post", post_uid=post.post_uid))
    return render_template("post_create.html", form=form)


@content_bp.get("/blog_posts/<post_uid>")
@content_bp.post("/blog_posts/<post_uid>")
def blog_post(post_uid=None):
    """This function dispatches control to the correct handler
    based on the URL and the query string

    Returns:
        Response: The Flask Response object with the rendered page
    """
    if request.args.get("action") is None:
        return blog_post_display(post_uid)
    elif request.args.get("action") == "update":
        return blog_post_update(post_uid)
    else:
        abort(404)


def blog_post_display(post_uid):
    """Content blog post page, presents a blog post based
    on the post_uid to the user that are clickable for
    the full post page

    Returns:
        text: the rendered HTML for the page
    """
    logger.debug("rendering blog post page")
    form = PostCommentForm()
    with db_session_manager() as db_session:
        # build the list of filters here to use in the CTE
        filters = [
            Post.post_uid == post_uid,
            Post.parent_uid is None
        ]
        if current_user.is_anonymous or current_user.can_view_posts():
            filters.append(Post.active == True)

        # build the recursive CTE query
        hierarchy = (
            db_session
            .query(Post, Post.sort_key.label("sorting_key"))
            .filter(*filters)
            .cte(name='hierarchy', recursive=True)
        )
        children = aliased(Post, name="c")
        hierarchy = hierarchy.union_all(
            db_session
            .query(
                children,
                (hierarchy.c.sorting_key + " " + children.sort_key).label("sorting_key")
            )
            .filter(children.parent_uid == hierarchy.c.post_uid)
        )
        # query the hierarchy for the post and it's comments
        posts = (
            db_session
            .query(Post, hierarchy.c.sorting_key)
            .select_entity_from(hierarchy)
            .order_by(hierarchy.c.sorting_key)
            .all()
        )
        if posts is None:
            flash(f"Unknown post uid: {post_uid}")
            abort(404)
        return render_template("post.html", form=form, posts=posts)


@login_required
def blog_post_update(post_uid=None):
    """Provides a mechanism to update blog post content

    Returns:
        text: the rendered HTML for the page
    """
    logger.debug("rendering blog post edit update page")
    with db_session_manager() as db_session:
        post = (
            db_session.query(Post)
            .options(db.joinedload("user"))
            .filter(Post.post_uid == post_uid)
        )
        # can the current user view only active posts:
        if current_user.is_anonymous or current_user.can_view_posts():
            post = post.filter(Post.active == True)
        post = post.one_or_none()
        if post is None:
            flash(f"Unknown post uid: {post_uid}")
            abort(404)
        form = PostUpdateForm(obj=post)
        if form.cancel.data:
            return redirect(url_for("intro_bp.home"))
        if form.validate_on_submit():
            post.title = form.title.data.strip()
            post.content = form.content.data.strip()
            if form.activate.data:
                post.active = True
            elif form.deactivate.data:
                post.active = False
            db_session.commit()
            flash(f"Blog post '{form.title.data.strip()}' updated")
        return render_template("post_update.html", form=form, post=post)


@content_bp.post("/blog_post_create_comment")
def blog_post_create_comment():
    form = PostCommentForm()
    if form.validate_on_submit():
        with db_session_manager() as db_session:
            post = Post(
                user_uid=current_user.user_uid,
                parent_uid=form.parent_post_uid.data,
                content=form.comment.data.strip(),
            )
            db_session.add(post)
            db_session.commit()
            root_post = post.parent
            while root_post.parent is not None:
                root_post = root_post.parent
            flash("Comment created")
            return redirect(url_for("content_bp.blog_post", post_uid=root_post.post_uid))
    else:
        flash("No comment to create")
    return redirect(url_for("intro_bp.home"))


@content_bp.context_processor
def utility_processor():
    """Add functionality to content templates
    """
    def can_update_blog_post(post):
        """Determines if the current user is the same as the
        the post creator, or if the current user is an
        administrator or editor

        Args:
            post (Post): The post object from the template

        Returns:
            Boolean: True if can update, False otherwise
        """
        if not current_user.is_anonymous:
            if current_user.role.permissions & (Role.Permissions.ADMINISTRATOR | Role.Permissions.EDITOR):
                return True
            if current_user.user_uid == post.user.user_uid:
                return True
        return False

    def can_set_blog_post_active_state(post):
        """Determines if the current user is the same as the
        the post creator, or if the current user is an
        administrator

        Args:
            post (Post): The post object from the template

        Returns:
            Boolean: True if can update, False otherwise
        """
        # is the current user anonymous?
        if current_user.is_anonymous:
            return False
        # is the current user an administrator or editor?
        if current_user.role.permissions & (Role.Permissions.ADMINISTRATOR):
            return True
        # otherwise, is the current user the creator of the post?
        else:
            if current_user.user_uid == post.user.user_uid:
                return True
        return False

    return dict(
        can_update_blog_post=can_update_blog_post,
        can_set_blog_post_active_state=can_set_blog_post_active_state,
    )
