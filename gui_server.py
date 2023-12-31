import os.path
import time
from functools import wraps

from flask import Flask, render_template, jsonify, request, redirect, make_response
from libmiyoushe import bbs, auth
from libmiyoushe import base as lib_base

import base

app = Flask(__name__)

color_mode = 'auto'

if os.path.exists('./_internal'):
    path_prefix = './_internal/'
else:
    path_prefix = './'

replace_list = [[r'<a href="https://(?:www\.miyoushe|bbs\.mihoyo|m\.miyoushe)\.com/.+?/article/(\d+)".+?target="_blank"', '<a onclick=showArticle({}) ']]


def verify_ua(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        return function(*args, **kwargs)

    return wrapper


@app.route('/dynamic_css')
@verify_ua
def dynamic_css():
    color_set = base.systemColorSet()[0]
    insert_css_text = ':root{--personal-color: ' + color_set + ' !important;}'
    with open(f'{path_prefix}static/app/css/dark.css') as f:
        match color_mode:
            case 'light':
                insert_css_text = insert_css_text
            case 'dark':
                insert_css_text += '\n' + f.read()
            case 'auto':
                insert_css_text += '\n@media (prefers-color-scheme: dark) {\n' + f.read() + '\n}'
            case _:
                pass
    resp = make_response(insert_css_text)
    resp.content_type = "text/css"
    return resp


@app.route('/favicon.ico')
@verify_ua
def favicon():
    return '404 Not Found', 404


@app.route('/<game>')
@verify_ua
def game_main(game):
    return render_template('homepage.html')


@app.route('/<game>/forum')
@verify_ua
def forum_page(game):
    return render_template('homepage.html')


@app.route('/<game>/vote')
def vote(game):
    return 'hello world'


@app.route('/api/<actions>', methods=['GET', 'POST'])
@verify_ua
def api(actions):
    match actions:
        case 'login':
            return ''
        case 'logout':
            return ''
        case 'homepage':
            page_type = request.args.get('type', 'feed')
            gid = request.args.get('gid', '2')
            page = request.args.get('page', '1')
            if not gid.isdigit():
                gid = str(bbs.getGame(gid)[1])
            match page_type:
                case 'feed':
                    articles = bbs.Page(gid, page_type)
                    return jsonify({'articles': articles.articles, 'last_id': '#!self_add!#'})
                case 'official':
                    official_type = request.args.get('official_type', 'news')
                    articles = bbs.Page(gid, official_type, page)

                    return jsonify({'articles': articles.articles, 'last_id': '#!self_add!#'})
                case 'forum':
                    forum_id = request.args.get('forum_id', '26')
                    forum = bbs.Forum(forum_id, gid, page, sort_type=1)
                    return jsonify({'articles': forum.articles, 'last_id': str(forum.last_id)})
                case _:
                    return '405 Method Not Allowed', 405
        case 'forum_list':
            gid = request.args.get('gid', '-1')
            if gid.isdigit() and gid != '-1':
                forum_list = bbs.Forum.getAllForum()[gid] if gid != '-1' else bbs.Forum.getAllForum()
                return jsonify(forum_list)
            elif gid == '-1':
                forum_list = bbs.Forum.getAllForum()
                return jsonify(forum_list)
            else:
                forum_list = bbs.Forum.getAllForum()[str(bbs.getGame(gid)[1])]
                return jsonify(forum_list)
        case 'game_list':
            query_game = request.args.get('game', 'all')
            return jsonify(bbs.getGame(query_game))
        case 'current_user':
            return jsonify({'nickname': '未登录', "uid": '0', "avatar": 'https://bbs-static.miyoushe.com/avatar/avatarDefault.png', 'isLogin': False})
        case 'article':
            post_id = request.args.get('post_id')
            article_action = request.args.get('action', 'raw')
            article = bbs.Article(post_id, replace_list)
            match article_action:
                case 'raw':
                    return article.result
                case _:
                    return '405 Method Not Allowed', 405

        case 'comment':
            page_id = request.args.get('post_id')
            gid = request.args.get('gid')
            page = request.args.get('page', '1')
            rank_by = request.args.get('rank_by', 'hot')
            if not gid.isdigit():
                gid = str(bbs.getGame(gid)[1])
            match rank_by:
                case 'earliest':
                    comment = bbs.Comments(page_id, gid, page, orderby=1, rank_by_hot=False)
                case 'latest':
                    comment = bbs.Comments(page_id, gid, page, orderby=2, rank_by_hot=False)
                case 'master':
                    comment = bbs.Comments(page_id, gid, page, only_master=True, rank_by_hot=False)
                case _:
                    comment = bbs.Comments(page_id, gid, page, rank_by_hot=True)
            return {
                'comments': comment.comments,
                'is_last': comment.isLastFlag
            }

        case 'validate':
            match request.args.get('method', 'create'):
                case 'create':
                    return auth.GeetestVerification.createVerification()
                case 'verify':
                    if request.method.upper() == 'POST':
                        result = auth.GeetestVerification.verifyVerification(request.json)
                        return result
                    else:
                        return '405 Method Not Allowed', 405

        case _:
            return '405 Method Not Allowed', 405


@app.route('/app-api/<actions>')
def app_api(actions):
    match actions:
        case 'app_config':
            config = {'version': base.app_version, 'cloud_conn': True, 'demo_mode': True, 'first_open': base.first_open, 'color_mode': color_mode}
            base.first_open = False
            return config
        case 'heartbeat':
            return {'t': int(time.time() * 1000)}
        case 'connection_test':
            return str(lib_base.connectionTest()).lower()
        case _:
            return '405 Method Not Allowed', 405


@app.route('/')
@verify_ua
def main():
    return redirect('/ys')


@app.errorhandler(Exception)
def pageError(err):
    if 'Connection Failed!' in str(err):
        return 'Connection Failed!', 503
    elif 'Authentication error' in str(err):
        return 'Authentication Error', 403