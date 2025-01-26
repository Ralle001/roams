# Project Name

A brief description of the project goes here.

## Installation

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/Ralle001/roams.git
   ```

2. Navigate into the project folder:
   ```bash
   cd roams
   ```

3. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   ```

4. Activate the virtual environment:
    Linux/Mac:
   ```bash
   source .venv/bin/activate
   ```

    Windows:
   ```bash
   .venv\Scripts\activate
   ```

5. Install the required dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

6. Start the application:
   ```bash
   python3 app.py
   ```

7. Access the API at [http://localhost:5000](http://localhost:5000).

8. Explore the Swagger documentation at [http://localhost:5000/swagger](http://localhost:5000/swagger).

## Usage

You can interact with the API using `curl`. Below are some examples:

#### Create User
```bash
curl -X POST http://localhost:5000/customers -H "Content-Type: application/json" -d "{\"name\":\"John Doe\",\"dni\":\"12345678Z\",\"email\":\"john@example.com\",\"requested_capital\":150000}"
```

#### Request User Data by DNI
```bash
curl -X GET http://localhost:5000/customers/12345678Z
```

#### Delete User by DNI
```bash
curl -X DELETE http://localhost:5000/customers/12345678Z
```

#### Update User Data by DNI
```bash
curl -X PUT http://localhost:5000/customers/12345678Z -H "Content-Type: application/json" -d "{\"name\":\"John Smith\",\"email\":\"johnsmith@example.com\"}"
```

#### Run Simulation by DNI
```bash
curl -X POST http://localhost:5000/customers/12345678Z/simulate -H "Content-Type: application/json" -d "{\"apr\":4.5,\"term_years\":20}"
