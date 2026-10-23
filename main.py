
print("OASIS integration started!")

state = "FOCUS"
print("Current state:", state)

from login_screen import OasisLoginOnly

if __name__ == "__main__":
    app = OasisLoginOnly()
    app.mainloop()
