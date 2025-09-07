from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from tools import tools_data
from badge_logic import assign_badge, generate_snapshot
from xion_integration import verify_user_xion, get_zktls_proof

app = Flask(__name__)
app.secret_key = "your_founder_secret_key"  # Replace with a secure key

@app.route("/")
def home():

    if not session.get("user_id"):
        return redirect(url_for("login"))

    # Your filtered_tools logic here...
    category = request.args.get("category")
    pricing = request.args.get("pricing")
    filtered_tools = {
        cat: [
            {
                **tool,
                "id": f"{cat[:3]}_{i}",
                "verified": True,
                "trust_score": 90,
                "fallback_triggered": False,
                "badge": assign_badge(tool),
            }
            for i, tool in enumerate(tools)
            if (not category or cat == category) and (not pricing or tool.get("pricing") == pricing)
        ]
        for cat, tools in tools_data.items()
    }
    return render_template("home.html", tools_data=filtered_tools)

@app.route("/dashboard")
def dashboard():
    all_tools = []
    for cat, tools in tools_data.items():
        for i, tool in enumerate(tools):
            tool["id"] = f"{cat[:3]}_{i}"
            tool["verified"] = True
            tool["trust_score"] = tool.get("trust_score") or 90
            tool["badge"] = assign_badge(tool) or "AI-Proof 🛡️"
            tool["fallback_triggered"] = False
            tool["snapshot"] = generate_snapshot(tool)
            all_tools.append(tool)
    return render_template("dashboard.html", tools=all_tools)

@app.route("/info")
def info():
    return render_template("info.html")

@app.route("/download")
def download():
    return "Download link coming soon!"  # Or redirect to GitHub/APK later

@app.route("/favorites")
def favorites():
    favorite_ids = request.args.getlist("ids")
    favorite_tools = []
    for cat, tools in tools_data.items():
        for i, tool in enumerate(tools):
            tool_id = f"{cat[:3]}_{i}"
            if tool_id in favorite_ids:
                tool["id"] = tool_id
                tool["verified"] = True
                tool["trust_score"] = 90
                tool["fallback_triggered"] = False
                tool["badge"] = assign_badge(tool)
                tool["snapshot"] = generate_snapshot(tool)
                favorite_tools.append(tool)
    return render_template("favorites.html", tools=favorite_tools)

@app.route("/favorite", methods=["POST"])
def favorite():
    data = request.get_json()
    tool_id = data.get("tool_id")
    return jsonify({"status": "success", "tool_id": tool_id})

@app.route("/rate", methods=["POST"])
def rate():
    data = request.get_json()
    tool_id = data.get("tool_id")
    value = data.get("value")
    return jsonify({"status": "rated", "tool_id": tool_id, "value": value})

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_id = request.form.get("username")
        session["user_id"] = user_id
        return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user_id = request.form.get("username")
        session["user_id"] = user_id
        return redirect(url_for("home"))
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
