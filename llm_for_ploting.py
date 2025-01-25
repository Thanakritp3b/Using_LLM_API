import numpy as np
import matplotlib.pyplot as plt
from mistralai import Mistral
import dotenv
import json
import os

dotenv.load_dotenv()

prompt_template = '''Return a JSON object for plotting mathematical functions. For polynomials, list coefficients from highest to lowest degree.

Examples:
- For "x^3 - 3x^2 + 5x - 1": {"function_type": "advanced", "function_name": "polynomial", "parameters": [1, -3, 5, -1], "x_min": -5, "x_max": 5, "exit": false}
- For "sin(x)": {"function_type": "basic", "function_name": "sin", "parameters": [], "x_min": -5, "x_max": 5, "exit": false}
- For "cos(2x)": {"function_type": "advanced", "function_name": "trig", "parameters": [2], "x_min": -5, "x_max": 5, "exit": false}
- For "goodbye": {"function_type": "none", "function_name": "none", "parameters": [], "x_min": 0, "x_max": 0, "exit": true}

User request: {user_input}

Return ONLY the JSON object.'''

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"
client = Mistral(api_key=api_key)

def extract_info(model, client, user_input):
   try:
       response = client.chat.complete(
           model=model,
           messages=[{
               "role": "user", 
               "content": prompt_template.replace("{user_input}", user_input)
           }]
       )
       response_text = response.choices[0].message.content.strip()
       print("LLM Response:", response_text)  #For debug but now it's work
       return json.loads(response_text)
   except Exception as e:
       print(f"Error parsing response: {e}")
       return {
           "function_type": "basic",
           "function_name": "sin",
           "parameters": [],
           "x_min": -5,
           "x_max": 5,
           "exit": False
       }

def plot_function(plot_info):
   x = np.linspace(plot_info["x_min"], plot_info["x_max"], 1000)
   
   if plot_info["function_type"] == "advanced" and plot_info["function_name"] == "polynomial":
       coeffs = plot_info["parameters"]
       y = np.polyval(coeffs, x)
   elif plot_info["function_type"] == "basic":
       if plot_info["function_name"] == "linear":
           y = x
       elif plot_info["function_name"] == "quadratic":
           y = x**2
       elif plot_info["function_name"] == "sin":
           y = np.sin(x)
       elif plot_info["function_name"] == "cos":
           y = np.cos(x)
   elif plot_info["function_type"] == "advanced" and plot_info["function_name"] == "trig":
       k = plot_info["parameters"][0]
       if "sin" in str(plot_info.get("function_name")).lower():
           y = np.sin(k * x)
       else:
           y = np.cos(k * x)
   
   plt.figure(figsize=(10, 6))
   plt.plot(x, y)
   plt.grid(True)
   plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
   plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)
   plt.title("Plot of requested function")
   plt.xlabel("x")
   plt.ylabel("y")
   plt.show()

def main():
   print("Welcome to the plotting application! What would you like to plot?")
   while True:
       user_input = input("Enter your plotting request (or say goodbye to exit): ")
       plot_info = extract_info(model, client, user_input)
       
       if plot_info["exit"]:
           print("Thank you for using the plotting application. Goodbye!")
           break
           
       try:
           plot_function(plot_info)
       except Exception as e:
           print(f"Error plotting function: {e}")
           continue

if __name__ == "__main__":
   main()