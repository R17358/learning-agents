from chatBot_memory import chat
from flask import Flask, request, jsonify, Response

# prompt = "Where is Europe"

# outputFile = "output.txt"

# result = chat(prompt)

# with open(outputFile, "w") as f:
#     f.write(result)

app = Flask(__name__)

@app.route('/api/hindi', methods=["POST"])
def hindi():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        print(prompt)
        output = chat(f" tell 5 lines on {prompt} in hindi")
        return jsonify({"status":"success", "response":output})
    except Exception as e:
        print(e)
        return jsonify({"error":e})

@app.route('/api/sanskrit', methods=["POST"])
def sanskrit():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        print(prompt)
        output = chat(f" tell 5 lines on {prompt} in sanskrit")
        return jsonify({"status":"success", "response":output})
    except Exception as e:
        return jsonify({"error":e})




if __name__ == "__main__":
    app.run(debug=True) 