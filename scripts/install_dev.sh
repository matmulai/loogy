#!/bin/bash
# Install package in development mode

# Navigate to the root directory
cd "$(dirname "$0")/.."

# Install package in development mode
pip install -e .

# Install additional requirements
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

echo "Package installed in development mode."
echo "You can now run:"
echo "  - Streamlit app: cd streamlit && streamlit run app.py"
echo "  - Benchmark: cd benchmark && python src/process_dataset.py" 