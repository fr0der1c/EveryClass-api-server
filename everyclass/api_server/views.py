from flask import Blueprint, flash, jsonify, redirect, request, url_for
from markupsafe import escape

from everyclass.api_server.exceptions import NoClassException, NoStudentException

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/_healthCheck')
def health_check():
    """健康检查"""
    return jsonify({"status": "ok"})


@main_blueprint.app_errorhandler(404)
def page_not_found(error):
    # 404跳转回首页
    # 404 errors are never handled on the blueprint level
    # unless raised from a view func so actual 404 errors,
    # i.e. "no route for it" defined, need to be handled
    # here on the application level
    if request.path.startswith('/api/'):
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    return redirect(url_for('main.main'))


# 405跳转回首页
@main_blueprint.app_errorhandler(405)
def method_not_allowed(error):
    return redirect(url_for('main.main'))


@main_blueprint.app_errorhandler(NoStudentException)
def no_student_exception_handle(error):
    flash('没有在数据库中找到你哦。是不是输错了？你刚刚输入的是%s' % escape(error))
    return redirect(url_for('main.main'))


@main_blueprint.app_errorhandler(NoClassException)
def no_class_exception_handle(error):
    flash('没有这门课程哦')
    return redirect(url_for('main.main'))
