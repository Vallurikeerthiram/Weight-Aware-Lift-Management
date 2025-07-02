# Elevator Optimization with Real-World Constraints: Weight-Aware Lift Management

A simulation-based desktop application built using **PyQt5** that models and optimizes **multi-lift operations** in high-rise buildings. The system uses real-world constraints like **weight capacity**, **passenger distribution**, and **floor distance** to **minimize wait time, energy consumption, and overload penalties**.

This project was presented at the **ICETESS Conference**.

---

##  Features

-  Weight-aware elevator dispatching
-  Smart load balancing across multiple lifts
-  Penalty-based optimization (wait time, energy, overload)
-  Mono control panel per floor (for real-world deployment modeling)
-  Adjustable number of floors, lifts, and capacities
-  Floor request buttons (up/down) per floor
-  Inside-lift passenger exit + destination handling

---

## Algorithms Used

- Greedy Search: Closest lift to target floor
- Nearest Neighbor: Based on direction & floor distance
- Overload Handling: Split passenger weight across lifts
- Centralized Controller: One panel for all elevators

---

## Simulation Setup

### Requirements

- Python 3.6+
- PyQt5

Install dependencies using:

```bash
pip install PyQt5
```

### Run the App

```bash
python lift_simulation.py
```

> On launch, the app will ask for:
> - Number of lifts
> - Lift capacity (kg)
> - Average person weight
> - Total floors

You can then interact with:
- Floor call buttons (Up/Down)
- Lift inside control panel to set destinations
- Passenger entry/exit tracking

---

## Sample Use Case

- Request 5 passengers on 6th floor  
- App calculates total weight  
- Chooses the closest lift(s) with available capacity  
- Moves lift to requested floor  
- Enter target floor and passenger exits  
- UI updates real-time floor & weight info

---

## Optimization Model

**Objective Function:**
```
Z = ∑ (w1 * Twait + w2 * Emove + w3 * Ooverload)
```

Where:
- `Twait`: Wait time = |Current floor - Requested floor|
- `Emove`: Energy = |Current floor - Target floor|
- `Ooverload`: Penalty if weight exceeds capacity
- `w1, w2, w3`: Weighting coefficients

---

##  Screenshots

> *(Insert UI screenshots here if available)*

---

##  Author

**Valluri Keerthi Ram**  
B.Tech CSE @ Amrita Vishwa Vidyapeetham  
keerthiramvalluri@gmail.com  
Bangalore, India

---

## Future Work

- Pressure/IoT sensor-based weight estimation
- Camera-based passenger count
- ML for adaptive elevator dispatching
- Voice or gesture-based floor requests

---

## License

MIT License
