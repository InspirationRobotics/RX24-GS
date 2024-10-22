from flask import Flask, render_template, request, jsonify

class FlaskApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.colors = ["#000000", "#000000", "#000000"]
        self.counter = 0
        self.frames = 0
        self.setup_routes()
        # Color map for the letter-to-color conversion
        self.color_map = {
            'N': '#000000',  # Black
            'R': '#FF0000',  # Red
            'B': '#0000FF',  # Blue
            'G': '#00FF00'   # Green
        }

    def setup_routes(self):
        # Route to display the colors
        @self.app.route('/')
        def display_colors():
            return render_template('STC.html', colors=self.colors, counter=self.counter, frames=self.frames)

        # API route to update colors
        @self.app.route('/update_colors', methods=['POST'])
        def update_colors():
            return self.update_colors_handler()

    def update_colors_handler(self):
        # Expecting a string like "NRB" where N=Black, R=Red, B=Blue
        color_string = request.json.get('colors')  # String of letters like "NRG"
        new_counter = request.json.get('counter')
        new_frames = request.json.get('frames')

        # Ensure the color string is 3 letters long
        if len(color_string) == 3:
            try:
                # Convert the color_string letters to hex codes using color_map
                new_colors = [self.color_map[char] for char in color_string]
                self.colors = new_colors
                self.counter = new_counter
                self.frames = new_frames
                return jsonify({"status": "success", "colors": self.colors, "counter": self.counter, "frames": self.frames})
            except KeyError:
                # Handle invalid letters that aren't in the color map
                return jsonify({"status": "error", "message": "Invalid color code provided. Use N, R, B, or G."}), 400
        else:
            return jsonify({"status": "error", "message": "Please provide a string of exactly 3 color codes."}), 400


    def run(self, debug=True):
        self.app.run(debug=debug)

# To run the server
# if __name__ == '__main__':
#     app_instance = FlaskApp()
#     app_instance.run()
