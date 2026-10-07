from flask import Flask

app = Flask(__name__)

app.json.ensure_ascii = False

STUDENTS = {
    "23T1020054": {
        "name": "Tran Quang Binh",
        "lop": "MMT",
        "scores": {"PMMNM": 8.5, "CSDL": 7.0, "MMT": 9.0}
    },
    "23T1020055": {
        "name": "Trần Quang Anh",
        "lop": "MMT",
        "scores": {"PMMNM": 6.0, "CSDL": 5.5, "MMT": 7.0}
    },
    "23T1020056": {
        "name": "Lê Hoàng Cường",
        "lop": "K47A",
        "scores": {"PMMNM": 9.5, "CSDL": 9.0}
    },
    "23T1020057": {
        "name": "Phạm Minh Dũng",
        "lop": "K47B",
        "scores": {"PMMNM": 4.0, "CSDL": 3.5, "MMT": 5.0}
    },
    "23T1020058": {
        "name": "Hoàng Thu Hà",
        "lop": "K47A",
        "scores": {}
    },
    "23T1020059": {
        "name": "Võ Quốc Khánh",
        "lop": "K47C",
        "scores": {"PMMNM": 7.5, "MMT": 8.0}
    }
}

def average(scores):
    if not scores:
        return None
    return round(sum(scores.values()) / len(scores), 2)

# 0.3 Hàm xếp loại
def rank(avg):
    if avg is None:
        return "Chưa có điểm"
    if avg >= 8.5:
        return "Giỏi"
    if avg >= 7.0:
        return "Khá"
    if avg >= 5.0:
        return "Trung bình"
    return "Yếu"
def student_summary(mssv):
    if mssv not in STUDENTS:
        return None
    info = STUDENTS[mssv]
    avg = average(info["scores"])
    return {
        "mssv": mssv,
        "name": info["name"],
        "lop": info["lop"],
        "scores": info["scores"],
        "average": avg,
        "rank": rank(avg)
    }
def layout(title, body):
    from markupsafe import escape
    safe_title = escape(title)
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>{safe_title} - Sổ điểm</title>
    <style>
        body {{ font-family: sans-serif; margin: 20px; line-height: 1.5; }}
        nav {{ margin-bottom: 20px; background: #f0f0f0; padding: 10px; }}
        nav a {{ margin-right: 15px; text-decoration: none; color: #0066cc; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 10px; }}
        th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
        th {{ background: #eee; }}
    </style>
</head>
<body>
    <nav>
        <a href="/">Trang chủ</a>
        <a href="/students">Sinh viên</a>
        <a href="/search">Tìm kiếm</a>
    </nav>
    <h1>{safe_title}</h1>
    <hr>
    <div>
        {body}
    </div>
</body>
</html>"""
if __name__ == "__main__":
    app.run(port=8000, debug=True)
    @app.route("/")
def home():

    total_students = len(STUDENTS)

    classes = {
        student["lop"]
        for student in STUDENTS.values()
    }

    total_classes = len(classes)

    body = f"""
        <h1>Sổ điểm lớp học</h1>

        <p>
            Tổng số sinh viên:
            <strong>{total_students}</strong>
        </p>

        <p>
            Số lớp:
            <strong>{total_classes}</strong>
        </p>

        <p>
            <a href="{url_for('student_list')}">
                Xem danh sách sinh viên
            </a>
        </p>

        <p>
            <a href="{url_for('api_students')}">
                API danh sách sinh viên
            </a>
        </p>
    """

    return layout(
        "Trang chủ",
        body
    )


# CÂU 2 - DANH SÁCH SINH VIÊN

@app.route("/students")
def student_list():

    selected_class = request.args.get(
        "lop",
        ""
    )

    classes = sorted({
        student["lop"]
        for student in STUDENTS.values()
    })

    if selected_class:

        student_ids = [
            mssv
            for mssv, student in STUDENTS.items()
            if student["lop"].lower()
            == selected_class.lower()
        ]

    else:

        student_ids = list(
            STUDENTS.keys()
        )

    body = """
        <h1>Danh sách sinh viên</h1>
    """

    body += f"""
        <p>

            <a href="{url_for('student_list')}">
                Tất cả
            </a>
    """

    for lop in classes:

        body += f"""
            |

            <a href="{url_for(
                'student_list',
                lop=lop
            )}">
                {escape(lop)}
            </a>
        """

    body += "</p>"

    if not student_ids:

        body += """
            <p>
                Không có sinh viên phù hợp.
            </p>
        """

        return layout(
            "Danh sách sinh viên",
            body
        )

    body += """
        <table border="1">

            <tr>
                <th>MSSV</th>
                <th>Họ tên</th>
                <th>Lớp</th>
                <th>Điểm TB</th>
                <th>Xếp loại</th>
            </tr>
    """

    for mssv in student_ids:

        summary = student_summary(
            mssv
        )

        if summary["average"] is None:
            avg_text = "—"
        else:
            avg_text = str(
                summary["average"]
            )

        body += f"""
            <tr>

                <td>
                    <a href="{url_for(
                        'student_detail',
                        mssv=mssv
                    )}">
                        {escape(mssv)}
                    </a>
                </td>

                <td>
                    {escape(summary["name"])}
                </td>

                <td>
                    {escape(summary["lop"])}
                </td>

                <td>
                    {escape(avg_text)}
                </td>

                <td>
                    {escape(summary["rank"])}
                </td>

            </tr>
        """

    body += "</table>"

    return layout(
        "Danh sách sinh viên",
        body
    )


# CÂU 3 - CHI TIẾT SINH VIÊN

@app.route("/students/<mssv>")
def student_detail(mssv):

    if mssv not in STUDENTS:

        abort(
            404,
            description=(
                f"Không có sinh viên "
                f"với MSSV = {mssv}."
            )
        )

    summary = student_summary(
        mssv
    )

    if summary["average"] is None:
        avg_text = "—"
    else:
        avg_text = str(
            summary["average"]
        )

    body = f"""
        <h1>Chi tiết sinh viên</h1>

        <p>
            <strong>Họ tên:</strong>
            {escape(summary["name"])}
        </p>

        <p>
            <strong>MSSV:</strong>
            {escape(summary["mssv"])}
        </p>

        <p>
            <strong>Lớp:</strong>

            <a href="{url_for(
                'student_list',
                lop=summary['lop']
            )}">
                {escape(summary["lop"])}
            </a>
        </p>

        <p>
            <strong>Điểm trung bình:</strong>
            {escape(avg_text)}
        </p>

        <p>
            <strong>Xếp loại:</strong>
            {escape(summary["rank"])}
        </p>

        <h2>Bảng điểm</h2>
    """

    if not summary["scores"]:

        body += """
            <p>Chưa có điểm.</p>
        """

    else:

        body += """
            <table border="1">

                <tr>
                    <th>Học phần</th>
                    <th>Điểm</th>
                </tr>
        """

        for course, score in summary["scores"].items():

            body += f"""
                <tr>
                    <td>{escape(course)}</td>
                    <td>{escape(str(score))}</td>
                </tr>
            """

        body += "</table>"

    body += f"""
        <p>

            <a href="{url_for(
                'export_scores',
                mssv=mssv
            )}">
                Tải bảng điểm (CSV)
            </a>

        </p>
    """

    short_url = url_for(
        "short_student",
        mssv=mssv
    )

    body += f"""
        <p>
            Link rút gọn:

            <a href="{short_url}">
                {escape(short_url)}
            </a>

        </p>
    """

    return layout(
        "Chi tiết sinh viên",
        body
    )


# CÂU 4 - REDIRECT 301

@app.route("/sv/<mssv>")
def short_student(mssv):

    return redirect(
        url_for(
            "student_detail",
            mssv=mssv
        ),
        code=301
    )


# CÂU 5 - EXPORT CSV

@app.route("/students/<mssv>/export")
def export_scores(mssv):

    if mssv not in STUDENTS:

        abort(
            404,
            description=(
                f"Không có sinh viên "
                f"với MSSV = {mssv}."
            )
        )

    student = STUDENTS[mssv]

    csv_content = "hoc_phan,diem\n"

    for course, score in student["scores"].items():

        csv_content += (
            f"{course},{score}\n"
        )

    response = make_response(
        csv_content
    )

    response.headers[
        "Content-Type"
    ] = "text/csv; charset=utf-8"

    response.headers[
        "Content-Disposition"
    ] = (
        f"attachment; "
        f"filename=diem_{mssv}.csv"
    )

    return response


# CÂU 6 - TÌM KIẾM

@app.route("/search")
def search():

    q = request.args.get(
        "q",
        ""
    )

    results = []

    if q:

        q_lower = q.lower()

        for mssv, student in STUDENTS.items():

            name_match = (
                q_lower
                in student["name"].lower()
            )

            mssv_match = (
                q_lower
                in mssv.lower()
            )

            if name_match or mssv_match:

                results.append(
                    mssv
                )

    body = f"""
        <h1>Tìm kiếm sinh viên</h1>

        <form
            method="GET"
            action="{url_for('search')}"
        >

            <input
                type="text"
                name="q"
                value="{escape(q)}"
                placeholder="Nhập tên hoặc MSSV"
            >

            <button type="submit">
                Tìm kiếm
            </button>

        </form>
    """

    if q:

        body += f"""
            <h2>
                Tìm thấy
                {len(results)}
                kết quả cho
                “{escape(q)}”
            </h2>
        """

        if results:

            body += "<ul>"

            for mssv in results:

                student = STUDENTS[mssv]

                body += f"""
                    <li>

                        <a href="{url_for(
                            'student_detail',
                            mssv=mssv
                        )}">

                            {escape(mssv)}
                            -
                            {escape(student["name"])}

                        </a>

                    </li>
                """

            body += "</ul>"

    return layout(
        "Tìm kiếm sinh viên",
        body
    )


# CÂU 7 - GET /api/students

@app.route("/api/students")
def api_students():

    lop = request.args.get(
        "lop"
    )

    min_avg = None

    if "min_avg" in request.args:

        min_avg_raw = request.args.get(
            "min_avg"
        )

        try:
            min_avg = float(
                min_avg_raw
            )

        except (TypeError, ValueError):

            abort(
                400,
                description=(
                    "min_avg phải là số."
                )
            )

    results = []

    for mssv, student in STUDENTS.items():

        summary = student_summary(
            mssv
        )

        if lop is not None:

            if (
                student["lop"].lower()
                != lop.lower()
            ):
                continue

        if min_avg is not None:

            if summary["average"] is None:
                continue

            if summary["average"] < min_avg:
                continue

        results.append(
            summary
        )

    return jsonify(
        results
    )


# CÂU 7 - GET /api/students/<mssv>

@app.route("/api/students/<mssv>")
def api_student_detail(mssv):

    if mssv not in STUDENTS:

        abort(
            404,
            description=(
                f"Không có sinh viên "
                f"với MSSV = {mssv}."
            )
        )

    return jsonify(
        student_summary(mssv)
    )


# CÂU 8

@app.route(
    "/api/students/<mssv>/scores/<course>",
    methods=[
        "GET",
        "PUT",
        "DELETE"
    ]
)
def api_score(mssv, course):

    if mssv not in STUDENTS:

        abort(
            404,
            description=(
                f"Không có sinh viên "
                f"với MSSV = {mssv}."
            )
        )

    course = course.upper()

    scores = STUDENTS[mssv][
        "scores"
    ]

    if request.method == "GET":

        if course not in scores:

            abort(
                404,
                description=(
                    f"Sinh viên {mssv} "
                    f"chưa có điểm học phần "
                    f"{course}."
                )
            )

        return jsonify({
            "mssv": mssv,
            "course": course,
            "score": scores[course]
        })

    if request.method == "PUT":

        if "score" not in request.args:

            abort(
                400,
                description=(
                    "Thiếu tham số score."
                )
            )

        score_raw = request.args.get(
            "score"
        )

        try:

            score = float(
                score_raw
            )

        except (TypeError, ValueError):

            abort(
                400,
                description=(
                    "score phải là số."
                )
            )

        if score < 0 or score > 10:

            abort(
                400,
                description=(
                    "score phải nằm "
                    "trong khoảng từ 0 đến 10."
                )
            )

        existed = (
            course in scores
        )

        scores[course] = score

        avg = average(
            scores
        )

        data = {
            "mssv": mssv,
            "course": course,
            "score": score,
            "average": avg
        }

        if existed:

            return jsonify(
                data
            ), 200

        response = make_response(
            jsonify(data),
            201
        )

        response.headers[
            "Location"
        ] = url_for(
            "api_score",
            mssv=mssv,
            course=course
        )

        return response

    if request.method == "DELETE":

        if course not in scores:

            abort(
                404,
                description=(
                    f"Sinh viên {mssv} "
                    f"chưa có điểm học phần "
                    f"{course}."
                )
            )

        del scores[course]

        return "", 204


# CÂU 9 - XỬ LÝ LỖI

@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(405)
def handle_error(error):

    titles = {
        400: "Dữ liệu không hợp lệ",
        404: "Không tìm thấy",
        405: "Phương thức không được hỗ trợ"
    }

    title = titles.get(
        error.code,
        "Có lỗi xảy ra"
    )

    if request.path.startswith("/api/"):

        return jsonify({
            "error": title,
            "detail": error.description
        }), error.code

    body = f"""
        <h1>
            {error.code} - {escape(title)}
        </h1>

        <p>
            {escape(error.description)}
        </p>
    """

    return layout(
        title,
        body
    ), error.code