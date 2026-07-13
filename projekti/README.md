Demo accounts are created automatically by migrations:

- Username: `demo1`, Password: `demo1pass`, Balance: `1000.00`
- Username: `demo2`, Password: `demo2pass`, Balance: `500.00`

Setup:
```bash
python -m django migrate --settings=projekti.settings
python -m django runserver --settings=projekti.settings