# Project Name

A brief description of the project goes here.

## Installation

1. Clone the repository to your local machine:
   ```bash
   git clone <repository-url>
   ```

2. Navigate into the project folder:
   ```bash
   cd <project-folder>
   ```

3. Install the required dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

4. Start the application:
   ```bash
   python3 app.py
   ```

5. Access the API at [http://localhost:5000](http://localhost:5000).

6. Explore the Swagger documentation at [http://localhost:5000/swagger](http://localhost:5000/swagger).

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
