from quantopian.pipeline import Pipeline
from quantopian.research import run_pipeline
from quantopian.pipeline.data.builtin import USEquityPricing
from quantopian.pipeline.filters import Q1500US

universal_set = Q1500US()

from quantopian.pipeline.data import morningstar

sector = morningstar.asset_classification.morningstar_sector_code.latest

energy_sector_numbers = sector.eq(309)

from quantopian.pipeline.factors import SimpleMovingAverage, AverageDollarVolume

dollar_volume = AverageDollarVolume(window_length=30)
high_dollar_volume = dollar_volume.percentile_between(90,100)
top_open_price = USEquityPricing.open.latest.top(50, mask=high_dollar_volume)
high_close_price = USEquityPricing.close.latest.percentile_between(90, 100, mask=top_open_price)

def make_quant_pipeline():
    
    base_universal_set = Q1500US()
    energy_sector_numbers = sector.eq(309)
    base_energy_num = base_universal_set & energy_sector_numbers
    dollar_volume = AverageDollarVolume(window_length=30)
    high_dollar_volume = dollar_volume.percentile_between(95,100)
    top_half_base_energy_num = base_energy_num & high_dollar_volume
    mean_10_day = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=10, mask=top_half_base_energy_num)
    mean_30_day = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=30, mask=top_half_base_energy_num)
    percent_difference_factor = (mean_10_day - mean_30_day) / mean_30_day
    
    short = percent_difference_factor < 0
    longs = percent_difference_factor > 0
    
    securities_to_trade = (short | longs)
    
    return Pipeline(
        columns={
            'long': longs,
            'short': short,
            'percent_diff':percent_difference_factor
        },
        screen=securities_to_trade
    )

result = run_pipeline(make_quant_pipeline(), '2017-05-05', '2019q-05-05')

