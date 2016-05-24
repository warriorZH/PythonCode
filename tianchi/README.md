# tianchi music data mining #

##  1. ./test.py
> test code for tianchi data mining

##  2. ./datashow.py
> show data in figure

##  3. ./arimatest.py
> algorithm test for arima
###  3.1 data series
```
dta = pd.Series(s_dta[:123])    
dta.index = pd.Index(sm.tsa.datetools.dates_from_range('2001','2123')) 
```
### 3.2 diff->pacf/acf
```
dta= dta.diff(1)#我们已经知道要使用一阶差分的时间序列，之前判断差分的程序可以注释掉     
fig = plt.figure()  
ax1=fig.add_subplot(221) 
fig = sm.graphics.tsa.plot_acf(dta, lags=40, ax=ax1)
ax2 = fig.add_subplot(222) 
fig = sm.graphics.tsa.plot_pacf(dta, lags=40, ax=ax2) 
```
### 3.3 use ARIMA to predict(set order->fit->predict)
```
model = ARIMA(dta, order=(5,0,5)) 
result_AR = model.fit(disp=-1)   
pre_data = result_AR.predict('2074','2183',dynamic=False) 
```
### 3.4 figure

##  4. ./armatest.py
> algorithm test for arma
###  4.1 data series
```
dta = pd.Series(s_dta[:153])
dta.index = pd.Index(sm.tsa.datetools.dates_from_range('2001', '2153'))
```
### 4.2 diff->pacf/acf
```
dta = dta.diff(1)
plt.plot(dta.index,dta.values)
# print(dta.values)
plt.show()
#
fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(dta.values.squeeze(), lags=40, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(dta, lags=40, ax=ax2)
fig.show()
```
### 4.3 use ARIMA to predict(set order->fit->predict)
```
arma_mod30 = sm.tsa.ARMA(dta, (3, 3)).fit(trend="c", method="css-mle")
# get what you need for predicting one-step ahead
params = arma_mod30.params
residuals = arma_mod30.resid
p = arma_mod30.k_ar
q = arma_mod30.k_ma
k_exog = arma_mod30.k_exog
k_trend = arma_mod30.k_trend
steps = 30
pre_result = _arma_predict_out_of_sample(params, steps, residuals, p, q, k_trend, k_exog, endog=dta, exog=None, start=len(dta))
```
### 4.4 figure
```
print(pre_result)
plt.plot(s_dta[153:183])
plt.plot(pre_result)
plt.show()
```

