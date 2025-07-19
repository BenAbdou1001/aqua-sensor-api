# AquaTrack FastAPI Backend

## Overview
This FastAPI application serves as the real-time data streaming component for the AquaTrack system, handling KPI data for multiple tanks via WebSockets.

## Prerequisites
- Python (v3.9 or later)
- pip

## Installation
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## Endpoints
- `POST /webhook`
- `POST /start-monitoring`
- `POST /stop-monitoring`
- `WS /ws`

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
For support or inquiries, contact [your-email@example.com](mailto:your-email@example.com).
