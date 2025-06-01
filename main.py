# main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()

# For simplicity, use hardcoded data
users = {"john": "1234", "jane": "abcd"}
clinics = {
    "Cardiology": ["Dr. Heart", "Dr. Pulse"],
    "Pediatrics": ["Dr. Kid", "Dr. Child"],
    "General Practice": ["Dr. Smith", "Dr. Doe"]
}
doctor_schedules = {
    "Dr. Heart": ["10:00", "14:00", "16:00"],
    "Dr. Pulse": ["11:00", "15:00"],
    "Dr. Kid": ["09:00", "13:00"],
    "Dr. Child": ["10:30", "15:30"],
    "Dr. Smith": ["12:00", "17:00"],
    "Dr. Doe": ["09:30", "13:30"]
}

@app.get("/")
def read_root():
    return {"message": "Hospital Chatbot API is up!"}

@app.post("/chat")
async def chat_endpoint(req: Request):
    data = await req.json()
    user_input = data.get("user_input", "").lower()
    session = data.get("session", {})

    # Login handling
    if not session.get("authenticated"):
        if not session.get("username"):
            session["step"] = "ask_username"
            return {"bot_response": "Please enter your username:", "session": session}
        elif not session.get("password"):
            session["username"] = user_input
            session["step"] = "ask_password"
            return {"bot_response": "Please enter your password:", "session": session}
        else:
            username = session["username"]
            password = user_input
            if users.get(username) == password:
                session["authenticated"] = True
                session["step"] = "main_menu"
                return {"bot_response": f"Welcome {username}! What would you like to do? (book, cancel, update)", "session": session}
            else:
                session.clear()
                return {"bot_response": "Invalid credentials. Start again.", "session": session}

    # Main actions
    if session["step"] == "main_menu":
        if "book" in user_input:
            session["step"] = "ask_clinic"
            return {"bot_response": "Which clinic do you want to book with? (Cardiology, Pediatrics, General Practice)", "session": session}
        elif "cancel" in user_input:
            return {"bot_response": "Cancellation feature is coming soon!", "session": session}
        elif "update" in user_input:
            return {"bot_response": "Update feature is coming soon!", "session": session}
        else:
            return {"bot_response": "I didn't understand. Please choose: book, cancel, update.", "session": session}

    # Booking flow
    if session["step"] == "ask_clinic":
        chosen_clinic = user_input.capitalize()
        if chosen_clinic in clinics:
            session["clinic"] = chosen_clinic
            session["step"] = "ask_doctor"
            doctors = clinics[chosen_clinic]
            return {"bot_response": f"Available doctors: {', '.join(doctors)}", "session": session}
        else:
            return {"bot_response": "Invalid clinic. Choose from: Cardiology, Pediatrics, General Practice.", "session": session}

    if session["step"] == "ask_doctor":
        chosen_doctor = user_input
        if chosen_doctor in doctor_schedules:
            session["doctor"] = chosen_doctor
            session["step"] = "ask_time"
            slots = doctor_schedules[chosen_doctor]
            return {"bot_response": f"Available time slots for {chosen_doctor}: {', '.join(slots)}", "session": session}
        else:
            return {"bot_response": "Doctor not found. Please enter the doctor's name.", "session": session}

    if session["step"] == "ask_time":
        chosen_time = user_input
        if chosen_time in doctor_schedules.get(session["doctor"], []):
            session["step"] = "main_menu"  # reset
            return {"bot_response": f"Appointment booked at {chosen_time} with {session['doctor']}!", "session": session}
        else:
            return {"bot_response": "Invalid time slot. Please enter a valid time.", "session": session}

    return {"bot_response": "Sorry, something went wrong.", "session": session}
