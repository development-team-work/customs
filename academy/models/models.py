from odoo import models, fields, api,_
from .. import num2words

class Teachers(models.Model):
    _name = 'academy.teachers'

    name = fields.Char()
    num=fields.Float("taka")
    num2bn=fields.Char("words",compute="compute_words",translate="True",)
    @api.onchange('num')

    def compute_words(self):
        self.num2bn=num2words.num2words(self.num)

        """def compute_words(self):
        num_2_bd={'0':'শুন্য','1':'এক','2':'দুই','3':'তিন','4':'চার','5':'পাঁচ','6':'ছয়','7':'সাত','8':'আট', '9':'নয়',
                  '10':'দশ','11':'এগার','12':'বার','13':'তের','14':'চৌদ্দ','15':'পনের','16':'ষোল','17':'সতের','18':'আঠার','19':'ঊনিশ',
                  '20':'বিশ','21':'একুশ','22':'বাইশ','23':'তেইশ','24':'চব্বিশ','25':'পঁচিশ','26':'ছাব্বিশ','27':'সাতাশ','28':'আঠাশ','29':'ঊনত্রিশ',
                  '30':'ত্রিশ','31':'একত্রিশ','32':'বত্রিশ','33':'তেত্রিশ','34':'চৌত্রিশ','35':'পঁয়ত্রিশ','36':'ছত্রিশ','37':'সাঁইত্রিশ','38':'আটত্রিশ','39':'ঊনচল্লিশ',
                  '40':'চল্লিশ','41':'একচল্লিশ','42':'বিয়াল্লিশ','43':'তেতাল্লিশ','44':'চুয়াল্লিশ','45':'পঁয়তাল্লিশ','46':'ছেচল্লিশ','47':'সাতচল্লিশ','48':'আটচল্লিশ','49':'ঊনপঞ্চাশ',
                  '50':'পঞ্চাশ','51':'একান্ন','52':'বায়ান্ন','53':'তিপ্পান্ন','54':'চুয়ান্ন','55':'পঞ্চান্ন','56':'ছাপ্পান্ন','57':'সাতান্ন','58':'আটান্ন','59':'ঊনষাট',
                  '60':'ষাট','61':'একষট্টি','62':'বাষট্টি','63':'তেষট্টি','64':'চৌষট্টি','65':'পঁয়ষট্টি','66':'ছেষট্টি','67':'সাতষট্টি','68':'আটষট্টি','69':'ঊনসত্তর',
                  '70':'সত্তর','71':'একাত্তর','72':'বাহাত্তর','73':'তিয়াত্তর','74':'চুয়াত্তর','75':'পঁচাত্তর','76':'ছিয়াত্তর','77':'সাতাত্তর','78':'আটাত্তর','79':'ঊনআশি',
                  '80':'আশি','81':'একাশি','82':'বিরাশি','83':'তিরাশি','84':'চুরাশি','85':'পঁচাশি','86':'ছিয়াশি','87':'সাতাশি','88':'আটাশি','89':'ঊননব্বই',
                  '90':'নব্বই','91':'একানব্বই','92':'বিরানব্বই','93':'তিরানব্বই','94':'চুরানব্বই','95':'পঁচানব্বই','96':'ছিয়ানব্বই','97':'সাতানব্বই','98':'আটানব্বই','99':'নিরানব্বই'}
        num_2_decimal={'0':'শুন্য','1':'এক','2':'দুই','3':'তিন','4':'চার','5':'পাঁচ','6':'ছয়','7':'সাত','8':'আট', '9':'নয়'}
        hundred= "শত"
        thousand= "হাজার"
        lac= "লক্ষ"
        crore= "কোটি"
        if self.num:
            numbers=self.spell_bd(self.num)
            if int(numbers['tens'])>0:
                words=num_2_bd[numbers['tens']]
            if int(numbers['hundreds'])>0:
                words=num_2_bd[numbers['hundreds']]+" " +hundred+" "+ words
            if int(numbers['thous'])>0:
                words=num_2_bd[str(int(numbers['thous']))]+" " +thousand+" "+ words
            if int(numbers['lacs'])>0:
                words=num_2_bd[numbers['lacs']]+" " +lac+" "+ words
            if int(numbers['crores'])>0:
                words=num_2_bd[numbers['crores']]+" " +crore+" "+ words

        self.num2bn=words

    def explode(self,float):
        numbers={}
        text=str(float)
        length=len(text)
        text.find('.')
        parts=text.split('.')
        numbers['hole_num']=parts[0]
        try:
            numbers['fraction']=parts[1]
        except IndexError:
            numbers['fraction']=0

        numbers['length']=len(hole_num)
        return numbers
    def spell_bd(self,numbers):
        numbers=self.explode(float)
        hole_num=numbers['hole_num']
        if length>2:
            numbers['tens']=hole_num[-2:]
            hole_num=hole_num[:-2]

        else:
            numbers['tens']=hole_num
            return numbers
        length = len(hole_num)
        if length > 1:
            numbers['hundreds'] = hole_num[-1:]
            hole_num = hole_num[:-1]

        else:
            numbers['hundreds'] = hole_num
            return numbers
        length = len(hole_num)
        if length > 2:
            numbers['thous'] = hole_num[-2:]
            hole_num = hole_num[:-2]

        else:
            numbers['thous'] = hole_num
            return numbers
        length = len(hole_num)
        if length > 2:
            numbers['lacs'] = hole_num[-2:]
            hole_num = hole_num[:-2]

        else:
            numbers['lacs'] = hole_num
            return numbers
        length = len(hole_num)
        if length > 2:
            numbers['crores'] = hole_num[-2:]
            hole_num = hole_num[:-2]

        else:
            numbers['crores'] = hole_num
            return numbers


    """