# Round Trip Time Game

## Overview
This is a multiplayer reaction time game implemented using **Python** and **sockets (TCP)**. Two players compete to input randomly generated numbers as quickly as possible, with real-time scoring and latency (RTT) tracking.

## How It Works
- The **server** generates random numbers for each round.
- Each **client** must enter the displayed number as quickly as possible.
- The server records the **response time (RTT)** for each player.
- The player with the fastest correct response wins the round.
- The game consists of **3 rounds**, and the final score determines the winner.

## Features
- **Multiplayer (2-player) support** over TCP.
- **RTT measurement** to track reaction times.
- **Automatic disqualification** for incorrect or missing responses.
- **Disconnect handling** to end the game if a player leaves.

## Installation & Setup

### Prerequisites:
- Python 3.x installed
- Basic knowledge of command-line usage

### Steps:
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/reaction-time-game.git
   cd reaction-time-game
   ```

2. Run the **server** (host machine):
   ```bash
   python server_final.py
   ```

3. Run the **clients** (on two different terminals or machines):
   ```bash
   python client1_final.py
   python client2_final.py
   ```

4. The game will start automatically once both players connect.

## Gameplay Instructions
- After connecting, players will receive a countdown before the game starts.
- When a number appears on screen, **type and submit it as fast as possible**.
- The **faster** you respond, the **higher** your chance of winning the round.
- If a player **disconnects**, the game ends immediately.

## Expected Output
- Players will see the countdown, followed by three rounds of number inputs.
- At the end of the game, the server displays:
  - **Final scores**
  - **Winner announcement**
  - **Reaction time rankings** (from slowest to fastest)

## Example Output (Server):
```
Server is listening for incoming connections...
Game starting in: 00:05
The game has started!  
Round 1
Player 1: Time=0.527s
Player 2: Time=0.398s
Scores: 0-1
Final Score:
Player 1 - Player 2
    1    -    2
Player 2 is the Winner!
Good Game!!
```
