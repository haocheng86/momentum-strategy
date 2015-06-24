# *Momentum Strategy*

Codes are in the "codes" folder. 

- class `MomentumPortfolio` (`MP`) in momentumPortfolio.py is designed for stock picking
- getting and updating data is written separately. `MP` can read data from any source
- class `BackTest` in backTest.py is inherited from `MP` to perform backtest

## *To-do*

- rewrite the data loading and cleaning part, need to be able to maintain and extend easily. 问汪哥该做啥，怎么做
- backtest on Quantopian and compare results
- *codes need more comments*
