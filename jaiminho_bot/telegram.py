import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('telegram', __name__, url_prefix='/telegram')

@bp.route('/enel', methods=['GET'])
def enel_invoice():
    return 'enel ok'
