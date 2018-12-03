# coding=utf-8
from decimal import Decimal
import decimal
import math

print (decimal.getcontext())

# 打印结果：2.564999999999999946709294817992486059665679931640625
print Decimal(2.565)
# 2.565000000000000053394788591
print Decimal(2565)*Decimal(0.001)

# 直接进行精度控制，第三位是5的时候，ROUND_HALF_UP无法成功进位,因为0.005程序记录成了0.00499999
print Decimal(2.565).quantize(Decimal('0.00'),decimal.ROUND_HALF_UP)
print (Decimal(2565)*Decimal(0.001)).quantize(Decimal('0.00'),decimal.ROUND_HALF_UP)
print Decimal(2.565).quantize(Decimal('0.00'),decimal.ROUND_HALF_DOWN)
print (Decimal(2565)*Decimal(0.001)).quantize(Decimal('0.00'),decimal.ROUND_HALF_DOWN)
print Decimal(2.563).quantize(Decimal('0.00'),decimal.ROUND_UP)
print Decimal(2.567).quantize(Decimal('0.00'),decimal.ROUND_DOWN)


#最终解决方案，先保留6位，最后再保留2位，尽可能减少了最后一步不精准数字对结果的影响
print Decimal(145.875432)
print Decimal(145.875432).quantize(Decimal('0.00'),decimal.ROUND_HALF_UP)
print Decimal(145.875000).quantize(Decimal('0.00'),decimal.ROUND_HALF_DOWN)






