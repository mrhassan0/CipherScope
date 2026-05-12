import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse


BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BACKEND_DIR.parent
FRONTEND_DIR = PROJECT_DIR / "frontend"

sys.path.insert(0, str(BACKEND_DIR))

from analysis import performance_comparison
from classical import caesar_brute_force_attack
from classical import double_transposition
from classical import substitution
from public_key import ecc
from public_key import rsa
from symmetric import aes
from symmetric import des


def comparison_table():
    return [
        {
            "algorithm": "Substitution Cipher",
            "category": "Classical",
            "key_type": "26-letter fixed mapping",
            "security_note": "Weak because letter patterns remain visible.",
            "analysis": "Frequency analysis, heuristic frequency attack, and Caesar brute-force demo.",
        },
        {
            "algorithm": "Double Transposition",
            "category": "Classical",
            "key_type": "Two permutation keys",
            "security_note": "Stronger than simple substitution but weak by modern standards.",
            "analysis": "Frequency analysis plus permutation attack for small row/column sizes.",
        },
        {
            "algorithm": "DES",
            "category": "Symmetric",
            "key_type": "Auto-generated symmetric key",
            "security_note": "Historically important but weak today due to small key size.",
            "analysis": "Round keys and timing.",
        },
        {
            "algorithm": "AES",
            "category": "Symmetric",
            "key_type": "Auto-generated symmetric key",
            "security_note": "Modern and strong when implemented correctly.",
            "analysis": "Round keys and timing.",
        },
        {
            "algorithm": "RSA",
            "category": "Public-key",
            "key_type": "Public/private key pair",
            "security_note": "Security depends on the difficulty of factoring n.",
            "analysis": "Key size, timing, encryption/decryption, and factorization demo.",
        },
        {
            "algorithm": "ECC",
            "category": "Public-key",
            "key_type": "Private key and public point",
            "security_note": "Strong security with smaller keys compared with RSA.",
            "analysis": "Point generation, public key, and ECDH shared key. No attack demo.",
        },
    ]


class CryptoRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format_text, *args):
        return

    def send_json(self, data, status=200):
        body = json.dumps(data, indent=2).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_file(self, file_path, content_type):
        if not file_path.exists():
            self.send_error(404)
            return

        body = file_path.read_bytes()

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json(self):
        content_length = int(self.headers.get("Content-Length", 0))

        if content_length == 0:
            return {}

        body = self.rfile.read(content_length).decode("utf-8")
        return json.loads(body)

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/" or path == "/index.html":
            self.send_file(FRONTEND_DIR / "index.html", "text/html; charset=utf-8")
            return

        if path == "/style.css":
            self.send_file(FRONTEND_DIR / "style.css", "text/css; charset=utf-8")
            return

        if path == "/script.js":
            self.send_file(FRONTEND_DIR / "script.js", "application/javascript; charset=utf-8")
            return

        if path == "/api/health":
            self.send_json({"success": True, "message": "CipherScope backend is running."})
            return

        if path == "/api/comparison":
            self.send_json({"success": True, "result": comparison_table()})
            return

        if path == "/api/performance-comparison":
            self.send_json({"success": True, "result": performance_comparison.run_full_comparison()})
            return

        self.send_error(404)

    def do_POST(self):
        path = urlparse(self.path).path

        try:
            data = self.read_json()
            result = self.handle_api(path, data)
            self.send_json({"success": True, "result": result})
        except Exception as error:
            self.send_json({"success": False, "error": str(error)}, status=400)

    def handle_api(self, path, data):
        if path == "/api/substitution/encrypt":
            plaintext = data.get("plaintext", "")
            key = data.get("key", "")
            ciphertext = substitution.encrypt(plaintext, key)

            return {
                "ciphertext": ciphertext,
                "frequency_analysis": substitution.frequency(ciphertext),
            }

        if path == "/api/substitution/decrypt":
            ciphertext = data.get("ciphertext", "")
            key = data.get("key", "")
            plaintext = substitution.decrypt(ciphertext, key)

            return {
                "plaintext": plaintext,
            }

        if path == "/api/substitution/frequency":
            text = data.get("text", "")
            return substitution.frequency(text)

        if path == "/api/substitution/frequency-attack":
            ciphertext = data.get("ciphertext", "")
            return substitution.frequency_attack(ciphertext)

        if path == "/api/substitution/bruteforce":
            ciphertext = data.get("ciphertext", "")
            return caesar_brute_force_attack.brute_force(ciphertext)

        if path == "/api/double-transposition/encrypt":
            plaintext = data.get("plaintext", "")
            first_key = data.get("first_key", "")
            second_key = data.get("second_key", "")
            return double_transposition.encrypt(plaintext, first_key, second_key)

        if path == "/api/double-transposition/decrypt":
            ciphertext = data.get("ciphertext", "")
            first_key = data.get("first_key", "")
            second_key = data.get("second_key", "")
            return double_transposition.decrypt(ciphertext, first_key, second_key)

        if path == "/api/double-transposition/frequency":
            text = data.get("text", "")
            return double_transposition.frequency(text)

        if path == "/api/double-transposition/permutation-attack":
            ciphertext = data.get("ciphertext", "")
            return double_transposition.permutation_attack(ciphertext)

        if path == "/api/des/run":
            plaintext = data.get("plaintext", "")
            return des.run_des(plaintext)

        if path == "/api/des/encrypt":
            plaintext = data.get("plaintext", "")
            return des.encrypt_text(plaintext)

        if path == "/api/des/decrypt":
            ciphertext_hex = data.get("ciphertext_hex", "")
            key_hex = data.get("key_hex", "")
            return des.decrypt_text(ciphertext_hex, key_hex)

        if path == "/api/aes/run":
            plaintext = data.get("plaintext", "")
            return aes.run_aes(plaintext)

        if path == "/api/aes/encrypt":
            plaintext = data.get("plaintext", "")
            return aes.encrypt_text(plaintext)

        if path == "/api/aes/decrypt":
            ciphertext_hex = data.get("ciphertext_hex", "")
            key_hex = data.get("key_hex", "")
            return aes.decrypt_text(ciphertext_hex, key_hex)

        if path == "/api/rsa/generate-keys":
            key_size = data.get("key_size", 512)
            return rsa.generate_keys(key_size)

        if path == "/api/rsa/encrypt":
            plaintext = data.get("plaintext", "")
            e = data.get("e", "")
            n = data.get("n", "")
            return rsa.encrypt_message(plaintext, e, n)

        if path == "/api/rsa/decrypt":
            ciphertext = data.get("ciphertext", "")
            d = data.get("d", "")
            n = data.get("n", "")
            return rsa.decrypt_message(ciphertext, d, n)

        if path == "/api/rsa/factorization-attack":
            n = data.get("n", "")
            e = data.get("e", "")
            return rsa.factorization_attack(n, e)

        if path == "/api/ecc/points":
            p = data.get("p", "")
            a_value = data.get("a", "")
            b_value = data.get("b", "")
            return ecc.list_points(p, a_value, b_value)

        if path == "/api/ecc/generate-key":
            p = data.get("p", "")
            a_value = data.get("a", "")
            b_value = data.get("b", "")
            gx = data.get("gx", "")
            gy = data.get("gy", "")
            n = data.get("n", "")
            private_key = data.get("private_key", "")
            return ecc.generate_public_key(p, a_value, b_value, gx, gy, n, private_key)

        if path == "/api/ecc/ecdh":
            p = data.get("p", "")
            a_value = data.get("a", "")
            b_value = data.get("b", "")
            gx = data.get("gx", "")
            gy = data.get("gy", "")
            n = data.get("n", "")
            alice_private = data.get("alice_private", "")
            bob_private = data.get("bob_private", "")
            return ecc.run_ecdh(p, a_value, b_value, gx, gy, n, alice_private, bob_private)

        raise ValueError("Unknown API endpoint: " + path)


def run_server():
    port = 8000

    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    server = HTTPServer(("0.0.0.0", port), CryptoRequestHandler)
    print("CipherScope is running at http://localhost:" + str(port))
    server.serve_forever()


if __name__ == "__main__":
    run_server()
