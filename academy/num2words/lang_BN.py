# Copyright (c) 2003, Taro Ogawa.  All Rights Reserved.
# Copyright (c) 2013, Savoir-faire Linux inc.  All Rights Reserved.

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA

from __future__ import division, print_function, unicode_literals

from . import lang_EU


class Num2Word_BN(lang_EU.Num2Word_EU):
    def set_high_numwords(self, high):
        self.cards[10 ** 12] = "ট্রিলিয়ন"
        self.cards[10 ** 9] = "বিলিয়ন"
        self.cards[10 ** 7] = "কোটি"
        self.cards[10 ** 5] = "লক্ষ"



    def setup(self):
        super(Num2Word_BN, self).setup()

        self.negword = "বিয়োগ "
        self.pointword = "দশমিক"
        self.errmsg_nornum = "শুধুমাত্র নম্বরই কথায় প্রকাশ করা যায়."
        self.exclude_title = ["এবং", "দশমিক", "বিয়োগ"]

        self.mid_numwords = [(1000, "হাজার"), (100, "শত"),]
        self.low_numwords = ["নিরানব্বই","আটানব্বই","সাতানব্বই","ছিয়ানব্বই","পঁচানব্বই","চুরানব্বই","তিরানব্বই",
                             "বিরানব্বই","একানব্বই","নব্বই","ঊননব্বই","আটাশি","সাতাশি","ছিয়াশি","পঁচাশি","চুরাশি",
                             "তিরাশি","বিরাশি","একাশি","আশি","ঊনআশি","আটাত্তর","সাতাত্তর","ছিয়াত্তর","পঁচাত্তর","চুয়াত্তর","তিয়াত্তর",
                             "বাহাত্তর","একাত্তর","সত্তর","ঊনসত্তর","আটষট্টি","সাতষট্টি","ছেষট্টি","পঁয়ষট্টি","চৌষট্টি","তেষট্টি","বাষট্টি","একষট্টি",
                             "ষাট","ঊনষাট","আটান্ন","সাতান্ন","ছাপ্পান্ন","পঞ্চান্ন","চুয়ান্ন","তিপ্পান্ন","বায়ান্ন","একান্ন","পঞ্চাশ","ঊনপঞ্চাশ","আটচল্লিশ",
                             "সাতচল্লিশ","ছেচল্লিশ","পঁয়তাল্লিশ","চুয়াল্লিশ","তেতাল্লিশ","বিয়াল্লিশ","একচল্লিশ","চল্লিশ","ঊনচল্লিশ","আটত্রিশ","সাঁইত্রিশ","ছত্রিশ",
                             "পঁয়ত্রিশ","চৌত্রিশ","তেত্রিশ","বত্রিশ","একত্রিশ","ত্রিশ","ঊনত্রিশ","আঠাশ","সাতাশ","ছাব্বিশ","পঁচিশ",
                            "চব্বিশ","তেইশ","বাইশ","একুশ","বিশ", "উনিশ", "আঠার", "সতের",
                             "ষোল", "পনের", "চৌদ্দ", "তের",
                             "বার", "এগার", "দশ", "নয়", "আট",
                             "সাত", "ছয়", "পাঁচ", "চার", "তিন", "দুই",
                             "এক", "শুন্য"]
        #TODO here to input চতুর্থ,ষষ্ঠ ইত্যাদি
        self.ords = {"এক": "প্রথম",
                     "দুই": "দ্বিতীয়",
                     "তিন": "তৃতীয়",
                     "চার": "চতুর্থ",
                     "পাঁচ": "পঞ্চম",
                     "ছয়": "ষষ্ঠ",
                     "সাত": "সপ্তম",
                     "আট": "অষ্টম",
                     "নয়": "নবম",
                     "দশ": "দশম",
                     }

    def merge(self, lpair, rpair):
        ltext, lnum = lpair
        rtext, rnum = rpair
        if lnum == 1 and rnum < 100:
            return (rtext, rnum)
        elif 100 > lnum > rnum:
            return ("%s-%s" % (ltext, rtext), lnum + rnum)
        elif lnum >= 100 > rnum:
            return ("%s %s" % (ltext, rtext), lnum + rnum)
        elif rnum > lnum:
            return ("%s %s" % (ltext, rtext), lnum * rnum)
        return ("%s, %s" % (ltext, rtext), lnum + rnum)

    def to_ordinal(self, value):
        self.verify_ordinal(value)
        outwords = self.to_cardinal(value).split(" ")
        lastwords = outwords[-1].split("-")
        lastword = lastwords[-1].lower()
        try:
            lastword = self.ords[lastword]
        except KeyError:
            if lastword[-1] == "y":
                lastword = lastword[:-1] + "ie"
            lastword += "তম"
        lastwords[-1] = self.title(lastword)
        outwords[-1] = "-".join(lastwords)
        return " ".join(outwords)

    def to_ordinal_num(self, value):
        self.verify_ordinal(value)
        return "%s%s" % (value, self.to_ordinal(value)[-2:])

    def to_year(self, val, longval=True):
        if not (val // 100) % 10:
            return self.to_cardinal(val)
        return self.to_splitnum(val, hightxt="hundred", jointxt="and",
                                longval=longval)
