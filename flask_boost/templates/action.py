

@bp.route('/#{controller}/#{action}')
def #{action}():
    return render_template('#{controller}/#{action}/#{action}.html')
