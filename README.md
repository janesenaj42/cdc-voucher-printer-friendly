# CDC-VOUCHER-PRINTER-FRIENDLY

For less tech-savvy family members (and too inconvenient to go CCs to get physical printouts).

## Set-up
`
conda create --no-default-packages -n cdc-voucher-printer-friendly python=3.9
conda activate cdc-voucher-printer-friendly
python -m pip install -r requirements.txt
`

Set CDC voucher link 'https://voucher.redeem.gov.sg/<XXXXX>' in `WEB_PATH` in `main.py`. Do not commit the link!!!

## To run
`
python main.py
`
Vouchers in printer friendly formats will be saved in 4x2 plots in the `plots` folder.

Works for voucher distributed in early 2023.