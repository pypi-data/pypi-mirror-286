import sys #line:1
import time #line:2
import copy #line:3
from time import strftime #line:5
from time import gmtime #line:6
import pandas as pd #line:8
import numpy as np #line:9
from pandas .api .types import CategoricalDtype #line:10
import progressbar #line:11
import re #line:12
from textwrap import wrap #line:13
import seaborn as sns #line:14
import matplotlib .pyplot as plt #line:15
class cleverminer :#line:17
    version_string ="1.1.0"#line:19
    def __init__ (self ,**OOOOOO0O0000O0000 ):#line:21
        """
        Starts CleverMiner procedure. Either only prepares data to binary form or both prepare data and execute enhanced association rule mining task.

        CleverMiner encapsulates several procedures - 4ft-Miner, CF-Miner, SD4ft-Miner and UIC-Miner.

        See https://cleverminer.org for details

        :param kwargs: list of keyword arguments.

        Keyword arguments inlude:
            * **df** - pandas dataframe (mandatory)
            * **proc** - procedure name (mandatory if task to be performed); one of the strings '4ftMiner','CFMiner','SD4ftMiner','UICMiner'
            * **target** - target variable for histogram mining procedures (CF-Miner, UIC-Miner) - for them parameter is mandatory
            * **opts** - options
            * **cedents** - definition of cedents.

            Each cedent has attributes and their types, minimal and maximal length. Attribute can be subset, sequence (seq), left or right cut (lcut, rcut) or one category (one) and for each, minimal and maximal number of categories are specified.

            ========== ========== ============ ============ ========== =============
            Procedure  Antecedent Succedent    Condition    First set  Second set
                       *ante*     *succ*       *cond*       *frst*     *scnd*
            ========== ========== ============ ============ ========== =============
            4ftMiner   Mandatory  Mandatory    Optional
            SD4ftMiner Mandatory  Mandatory    Optional     Mandatory  Mandatory
            CFMiner                            Mandatory
            UICMiner   Mandatory               Optional
            ========== ========== ============ ============ ========== =============

        """#line:50
        self ._print_disclaimer ()#line:51
        self .stats ={'total_cnt':0 ,'total_ver':0 ,'total_valid':0 ,'control_number':0 ,'start_prep_time':time .time (),'end_prep_time':time .time (),'start_proc_time':time .time (),'end_proc_time':time .time ()}#line:60
        self .options ={'max_categories':100 ,'max_rules':None ,'optimizations':True ,'automatic_data_conversions':True ,'progressbar':True ,'keep_df':False }#line:68
        self .df =None #line:69
        self .kwargs =None #line:70
        if len (OOOOOO0O0000O0000 )>0 :#line:71
            self .kwargs =OOOOOO0O0000O0000 #line:72
        self .profiles ={}#line:73
        self .verbosity ={}#line:74
        self .verbosity ['debug']=False #line:75
        self .verbosity ['print_rules']=False #line:76
        self .verbosity ['print_hashes']=True #line:77
        self .verbosity ['last_hash_time']=0 #line:78
        self .verbosity ['hint']=False #line:79
        if "opts"in OOOOOO0O0000O0000 :#line:80
            self ._set_opts (OOOOOO0O0000O0000 .get ("opts"))#line:81
        if "opts"in OOOOOO0O0000O0000 :#line:82
            if "verbose"in OOOOOO0O0000O0000 .get ('opts'):#line:83
                OOO0O0OOO00OOO00O =OOOOOO0O0000O0000 .get ('opts').get ('verbose')#line:84
                if OOO0O0OOO00OOO00O .upper ()=='FULL':#line:85
                    self .verbosity ['debug']=True #line:86
                    self .verbosity ['print_rules']=True #line:87
                    self .verbosity ['print_hashes']=False #line:88
                    self .verbosity ['hint']=True #line:89
                    self .options ['progressbar']=False #line:90
                elif OOO0O0OOO00OOO00O .upper ()=='RULES':#line:91
                    self .verbosity ['debug']=False #line:92
                    self .verbosity ['print_rules']=True #line:93
                    self .verbosity ['print_hashes']=True #line:94
                    self .verbosity ['hint']=True #line:95
                    self .options ['progressbar']=False #line:96
                elif OOO0O0OOO00OOO00O .upper ()=='HINT':#line:97
                    self .verbosity ['debug']=False #line:98
                    self .verbosity ['print_rules']=False #line:99
                    self .verbosity ['print_hashes']=True #line:100
                    self .verbosity ['last_hash_time']=0 #line:101
                    self .verbosity ['hint']=True #line:102
                    self .options ['progressbar']=False #line:103
                elif OOO0O0OOO00OOO00O .upper ()=='DEBUG':#line:104
                    self .verbosity ['debug']=True #line:105
                    self .verbosity ['print_rules']=True #line:106
                    self .verbosity ['print_hashes']=True #line:107
                    self .verbosity ['last_hash_time']=0 #line:108
                    self .verbosity ['hint']=True #line:109
                    self .options ['progressbar']=False #line:110
        self ._is_py310 =sys .version_info [0 ]>=4 or (sys .version_info [0 ]>=3 and sys .version_info [1 ]>=10 )#line:111
        if not (self ._is_py310 ):#line:112
            print ("Warning: Python 3.10+ NOT detected. You should upgrade to Python 3.10 or greater to get better performance")#line:113
        else :#line:114
            if (self .verbosity ['debug']):#line:115
                print ("Python 3.10+ detected.")#line:116
        self ._initialized =False #line:117
        self ._init_data ()#line:118
        self ._init_task ()#line:119
        if len (OOOOOO0O0000O0000 )>0 :#line:120
            if "df"in OOOOOO0O0000O0000 :#line:121
                self ._prep_data (OOOOOO0O0000O0000 .get ("df"))#line:122
            else :#line:123
                print ("Missing dataframe. Cannot initialize.")#line:124
                self ._initialized =False #line:125
                return #line:126
            OO000000OOOO0O0OO =OOOOOO0O0000O0000 .get ("proc",None )#line:127
            if not (OO000000OOOO0O0OO ==None ):#line:128
                self ._calculate (**OOOOOO0O0000O0000 )#line:129
            else :#line:130
                if self .verbosity ['debug']:#line:131
                    print ("INFO: just initialized")#line:132
                OO0O0OOOO000O00OO ={}#line:133
                O000000000OO0OO00 ={}#line:134
                O000000000OO0OO00 ["varname"]=self .data ["varname"]#line:135
                O000000000OO0OO00 ["catnames"]=self .data ["catnames"]#line:136
                OO0O0OOOO000O00OO ["datalabels"]=O000000000OO0OO00 #line:137
                self .result =OO0O0OOOO000O00OO #line:138
        self ._initialized =True #line:140
    def _set_opts (self ,opts ):#line:142
        if "no_optimizations"in opts :#line:143
            self .options ['optimizations']=not (opts ['no_optimizations'])#line:144
            print ("No optimization will be made.")#line:145
        if "disable_progressbar"in opts :#line:146
            self .options ['progressbar']=False #line:147
            print ("Progressbar will not be shown.")#line:148
        if "max_rules"in opts :#line:149
            self .options ['max_rules']=opts ['max_rules']#line:150
        if "max_categories"in opts :#line:151
            self .options ['max_categories']=opts ['max_categories']#line:152
            if self .verbosity ['debug']==True :#line:153
                print (f"Maximum number of categories set to {self.options['max_categories']}")#line:154
        if "no_automatic_data_conversions"in opts :#line:155
            self .options ['automatic_data_conversions']=not (opts ['no_automatic_data_conversions'])#line:156
            print ("No automatic data conversions will be made.")#line:157
        if "keep_df"in opts :#line:158
            self .options ['keep_df']=opts ['keep_df']#line:159
    def _init_data (self ):#line:162
        self .data ={}#line:164
        self .data ["varname"]=[]#line:165
        self .data ["catnames"]=[]#line:166
        self .data ["vtypes"]=[]#line:167
        self .data ["dm"]=[]#line:168
        self .data ["rows_count"]=int (0 )#line:169
        self .data ["data_prepared"]=0 #line:170
    def _init_task (self ):#line:172
        if "opts"in self .kwargs :#line:174
            self ._set_opts (self .kwargs .get ("opts"))#line:175
        self .cedent ={'cedent_type':'none','defi':{},'num_cedent':0 ,'trace_cedent':[],'trace_cedent_asindata':[],'traces':[],'generated_string':'','rule':{},'filter_value':int (0 )}#line:185
        self .task_actinfo ={'proc':'','cedents_to_do':[],'cedents':[]}#line:189
        self .rulelist =[]#line:190
        self .stats ['total_cnt']=0 #line:191
        self .stats ['total_valid']=0 #line:192
        self .stats ['control_number']=0 #line:193
        self .result ={}#line:194
        self ._opt_base =None #line:195
        self ._opt_relbase =None #line:196
        self ._opt_base1 =None #line:197
        self ._opt_relbase1 =None #line:198
        self ._opt_base2 =None #line:199
        self ._opt_relbase2 =None #line:200
        OOO0O0O0O000OOO0O =None #line:201
        if not (self .kwargs ==None ):#line:202
            OOO0O0O0O000OOO0O =self .kwargs .get ("quantifiers",None )#line:203
            if not (OOO0O0O0O000OOO0O ==None ):#line:204
                for O0OOO000O000OO00O in OOO0O0O0O000OOO0O .keys ():#line:205
                    if O0OOO000O000OO00O .upper ()=='BASE':#line:206
                        self ._opt_base =OOO0O0O0O000OOO0O .get (O0OOO000O000OO00O )#line:207
                    if O0OOO000O000OO00O .upper ()=='RELBASE':#line:208
                        self ._opt_relbase =OOO0O0O0O000OOO0O .get (O0OOO000O000OO00O )#line:209
                    if (O0OOO000O000OO00O .upper ()=='FRSTBASE')|(O0OOO000O000OO00O .upper ()=='BASE1'):#line:210
                        self ._opt_base1 =OOO0O0O0O000OOO0O .get (O0OOO000O000OO00O )#line:211
                    if (O0OOO000O000OO00O .upper ()=='SCNDBASE')|(O0OOO000O000OO00O .upper ()=='BASE2'):#line:212
                        self ._opt_base2 =OOO0O0O0O000OOO0O .get (O0OOO000O000OO00O )#line:213
                    if (O0OOO000O000OO00O .upper ()=='FRSTRELBASE')|(O0OOO000O000OO00O .upper ()=='RELBASE1'):#line:214
                        self ._opt_relbase1 =OOO0O0O0O000OOO0O .get (O0OOO000O000OO00O )#line:215
                    if (O0OOO000O000OO00O .upper ()=='SCNDRELBASE')|(O0OOO000O000OO00O .upper ()=='RELBASE2'):#line:216
                        self ._opt_relbase2 =OOO0O0O0O000OOO0O .get (O0OOO000O000OO00O )#line:217
            else :#line:218
                print ("Warning: no quantifiers found. Optimization will not take place (1)")#line:219
        else :#line:220
            print ("Warning: no quantifiers found. Optimization will not take place (2)")#line:221
    def mine (self ,**OO00O00000O00O0OO ):#line:224
        """
        Runs a mining task on a prepared data set.
        :param kwargs: list of keyword arguments. List is the same as for mining task with default constructor.
        :return: a dictionary with task summary, task processing statistics, ruleset and variable information.
        """#line:229
        if not (self ._initialized ):#line:230
            print ("Class NOT INITIALIZED. Please call constructor with dataframe first")#line:231
            return #line:232
        self .kwargs =None #line:233
        if len (OO00O00000O00O0OO )>0 :#line:234
            self .kwargs =OO00O00000O00O0OO #line:235
        self ._init_task ()#line:236
        if len (OO00O00000O00O0OO )>0 :#line:237
            O00O0O000OOOOO00O =OO00O00000O00O0OO .get ("proc",None )#line:238
            if not (O00O0O000OOOOO00O ==None ):#line:239
                self ._calc_all (**OO00O00000O00O0OO )#line:240
            else :#line:241
                print ("Rule mining procedure missing")#line:242
    def _get_ver (self ):#line:245
        return self .version_string #line:246
    def _print_disclaimer (self ):#line:248
        print (f"Cleverminer version {self._get_ver()}.")#line:249
    def _automatic_data_conversions (self ,df ):#line:250
        print ("Automatically reordering numeric categories ...")#line:251
        for O0O0O0000O00OO0OO in range (len (df .columns )):#line:252
            if self .verbosity ['debug']:#line:253
                print (f"#{O0O0O0000O00OO0OO}: {df.columns[O0O0O0000O00OO0OO]} : {df.dtypes[O0O0O0000O00OO0OO]}.")#line:254
            try :#line:255
                df [df .columns [O0O0O0000O00OO0OO ]]=df [df .columns [O0O0O0000O00OO0OO ]].astype (str ).astype (float )#line:256
                if self .verbosity ['debug']:#line:257
                    print (f"CONVERTED TO FLOATS #{O0O0O0000O00OO0OO}: {df.columns[O0O0O0000O00OO0OO]} : {df.dtypes[O0O0O0000O00OO0OO]}.")#line:258
                O00O0OO000O0000O0 =pd .unique (df [df .columns [O0O0O0000O00OO0OO ]])#line:259
                OOO000OOOO000O000 =True #line:260
                for OOO0O0OOOO00OO0OO in O00O0OO000O0000O0 :#line:261
                    if OOO0O0OOOO00OO0OO %1 !=0 :#line:262
                        OOO000OOOO000O000 =False #line:263
                if OOO000OOOO000O000 :#line:264
                    df [df .columns [O0O0O0000O00OO0OO ]]=df [df .columns [O0O0O0000O00OO0OO ]].astype (int )#line:265
                    if self .verbosity ['debug']:#line:266
                        print (f"CONVERTED TO INT #{O0O0O0000O00OO0OO}: {df.columns[O0O0O0000O00OO0OO]} : {df.dtypes[O0O0O0000O00OO0OO]}.")#line:267
                O0O00OOO0OOOO0OO0 =pd .unique (df [df .columns [O0O0O0000O00OO0OO ]])#line:268
                O000000OO00OO00O0 =CategoricalDtype (categories =O0O00OOO0OOOO0OO0 .sort (),ordered =True )#line:269
                df [df .columns [O0O0O0000O00OO0OO ]]=df [df .columns [O0O0O0000O00OO0OO ]].astype (O000000OO00OO00O0 )#line:270
                if self .verbosity ['debug']:#line:271
                    print (f"CONVERTED TO CATEGORY #{O0O0O0000O00OO0OO}: {df.columns[O0O0O0000O00OO0OO]} : {df.dtypes[O0O0O0000O00OO0OO]}.")#line:272
            except :#line:274
                if self .verbosity ['debug']:#line:275
                    print ("...cannot be converted to int")#line:276
                try :#line:277
                    OOOO0O00OOO0OOOO0 =df [df .columns [O0O0O0000O00OO0OO ]].unique ()#line:278
                    if self .verbosity ['debug']:#line:279
                        print (f"Values: {OOOO0O00OOO0OOOO0}")#line:280
                    O0O000OO0O0000O0O =True #line:281
                    OOO0O00O00O0OOO0O =[]#line:282
                    for OOO0O0OOOO00OO0OO in OOOO0O00OOO0OOOO0 :#line:283
                        OOO0O00OO00OOOOOO =re .findall (r"-?\d+",OOO0O0OOOO00OO0OO )#line:286
                        if len (OOO0O00OO00OOOOOO )>0 :#line:288
                            OOO0O00O00O0OOO0O .append (int (OOO0O00OO00OOOOOO [0 ]))#line:289
                        else :#line:290
                            O0O000OO0O0000O0O =False #line:291
                    if self .verbosity ['debug']:#line:292
                        print (f"Is ok: {O0O000OO0O0000O0O}, extracted {OOO0O00O00O0OOO0O}")#line:293
                    if O0O000OO0O0000O0O :#line:294
                        OO0O0O0000OO000OO =copy .deepcopy (OOO0O00O00O0OOO0O )#line:295
                        OO0O0O0000OO000OO .sort ()#line:296
                        O0000OO0O000OOO0O =[]#line:298
                        for OO0O00000OOOOOOOO in OO0O0O0000OO000OO :#line:299
                            OOOO00O00O00O000O =OOO0O00O00O0OOO0O .index (OO0O00000OOOOOOOO )#line:300
                            O0000OO0O000OOO0O .append (OOOO0O00OOO0OOOO0 [OOOO00O00O00O000O ])#line:302
                        if self .verbosity ['debug']:#line:303
                            print (f"Sorted list: {O0000OO0O000OOO0O}")#line:304
                        O000000OO00OO00O0 =CategoricalDtype (categories =O0000OO0O000OOO0O ,ordered =True )#line:305
                        df [df .columns [O0O0O0000O00OO0OO ]]=df [df .columns [O0O0O0000O00OO0OO ]].astype (O000000OO00OO00O0 )#line:306
                except :#line:307
                    if self .verbosity ['debug']:#line:308
                        print ("...cannot extract numbers from all categories")#line:309
        print ("Automatically reordering numeric categories ...done")#line:311
    def _prep_data (self ,df ):#line:313
        print ("Starting data preparation ...")#line:314
        self ._init_data ()#line:315
        self .stats ['start_prep_time']=time .time ()#line:316
        if self .options ['automatic_data_conversions']:#line:317
            self ._automatic_data_conversions (df )#line:318
        self .data ["rows_count"]=df .shape [0 ]#line:319
        for O0O0OO0OOO000OOOO in df .select_dtypes (exclude =['category']).columns :#line:320
            df [O0O0OO0OOO000OOOO ]=df [O0O0OO0OOO000OOOO ].apply (str )#line:321
        try :#line:322
            O0O000O00OO0OOO00 =pd .DataFrame .from_records ([(O00000OOO00O0OOOO ,df [O00000OOO00O0OOOO ].nunique ())for O00000OOO00O0OOOO in df .columns ],columns =['Column_Name','Num_Unique']).sort_values (by =['Num_Unique'])#line:324
        except :#line:325
            print ("Error in input data, probably unsupported data type. Will try to scan for column with unsupported type.")#line:326
            OOO00OOOO0O0OOOO0 =""#line:327
            try :#line:328
                for O0O0OO0OOO000OOOO in df .columns :#line:329
                    OOO00OOOO0O0OOOO0 =O0O0OO0OOO000OOOO #line:330
                    print (f"...column {O0O0OO0OOO000OOOO} has {int(df[O0O0OO0OOO000OOOO].nunique())} values")#line:331
            except :#line:332
                print (f"... detected : column {OOO00OOOO0O0OOOO0} has unsupported type: {type(df[O0O0OO0OOO000OOOO])}.")#line:333
                exit (1 )#line:334
            print (f"Error in data profiling - attribute with unsupported type not detected. Please profile attributes manually, only simple attributes are supported.")#line:335
            exit (1 )#line:336
        if self .verbosity ['hint']:#line:339
            print ("Quick profile of input data: unique value counts are:")#line:340
            print (O0O000O00OO0OOO00 )#line:341
            for O0O0OO0OOO000OOOO in df .columns :#line:342
                if df [O0O0OO0OOO000OOOO ].nunique ()<self .options ['max_categories']:#line:343
                    df [O0O0OO0OOO000OOOO ]=df [O0O0OO0OOO000OOOO ].astype ('category')#line:344
                else :#line:345
                    print (f"WARNING: attribute {O0O0OO0OOO000OOOO} has more than {self.options['max_categories']} values, will be ignored.\r\n If you haven't set maximum number of categories and you really need more categories and you know what you are doing, please use max_categories option to increase allowed number of categories.")#line:346
                    del df [O0O0OO0OOO000OOOO ]#line:347
        for O0O0OO0OOO000OOOO in df .columns :#line:349
            if df [O0O0OO0OOO000OOOO ].nunique ()>self .options ['max_categories']:#line:350
                print (f"WARNING: attribute {O0O0OO0OOO000OOOO} has more than {self.options['max_categories']} values, will be ignored.\r\n If you haven't set maximum number of categories and you really need more categories and you know what you are doing, please use max_categories option to increase allowed number of categories.")#line:351
                del df [O0O0OO0OOO000OOOO ]#line:352
        if self .options ['keep_df']:#line:353
            if self .verbosity ['debug']:#line:354
                print ("Keeping df.")#line:355
            self .df =df #line:356
        print ("Encoding columns into bit-form...")#line:357
        O0OOOOOOOOO0OOOO0 =0 #line:358
        OOOOOOOO0OOO0000O =0 #line:359
        for O0000OO0O0OOO00OO in df :#line:360
            if self .verbosity ['debug']:#line:361
                print ('Column: '+O0000OO0O0OOO00OO +' @ '+str (time .time ()))#line:362
            if self .verbosity ['debug']:#line:363
                print ('Column: '+O0000OO0O0OOO00OO )#line:364
            self .data ["varname"].append (O0000OO0O0OOO00OO )#line:365
            O0OO000OOO0OO00OO =pd .get_dummies (df [O0000OO0O0OOO00OO ])#line:366
            OOO0O000OOO0OO0O0 =0 #line:367
            if (df .dtypes [O0000OO0O0OOO00OO ].name =='category'):#line:368
                OOO0O000OOO0OO0O0 =1 #line:369
            self .data ["vtypes"].append (OOO0O000OOO0OO0O0 )#line:370
            if self .verbosity ['debug']:#line:371
                print (O0OO000OOO0OO00OO )#line:372
                print (df [O0000OO0O0OOO00OO ])#line:373
            O0OOOOO00OOO0O00O =0 #line:374
            OOO0OO0OO0OOOO000 =[]#line:375
            O0O0O000OOO00OOOO =[]#line:376
            if self .verbosity ['debug']:#line:377
                print ('...starting categories '+str (time .time ()))#line:378
            for OO00O0O0OO00O0O0O in O0OO000OOO0OO00OO :#line:379
                if self .verbosity ['debug']:#line:380
                    print ('....category : '+str (OO00O0O0OO00O0O0O )+' @ '+str (time .time ()))#line:381
                OOO0OO0OO0OOOO000 .append (OO00O0O0OO00O0O0O )#line:382
                O0O0OO0O00OO0OOO0 =int (0 )#line:383
                OO0O00OO0OOOO000O =O0OO000OOO0OO00OO [OO00O0O0OO00O0O0O ].values #line:384
                if self .verbosity ['debug']:#line:385
                    print (OO0O00OO0OOOO000O .ndim )#line:386
                OOOOO00000O00OOO0 =np .packbits (OO0O00OO0OOOO000O ,bitorder ='little')#line:387
                O0O0OO0O00OO0OOO0 =int .from_bytes (OOOOO00000O00OOO0 ,byteorder ='little')#line:388
                O0O0O000OOO00OOOO .append (O0O0OO0O00OO0OOO0 )#line:389
                if self .verbosity ['debug']:#line:391
                    for O0000O0O000O0000O in range (self .data ["rows_count"]):#line:393
                        if OO0O00OO0OOOO000O [O0000O0O000O0000O ]>0 :#line:394
                            O0O0OO0O00OO0OOO0 +=1 <<O0000O0O000O0000O #line:395
                            O0O0O000OOO00OOOO .append (O0O0OO0O00OO0OOO0 )#line:396
                    print ('....category ATTEMPT 2: '+str (OO00O0O0OO00O0O0O )+" @ "+str (time .time ()))#line:399
                    O000OOO0O0OOOO00O =int (0 )#line:400
                    O00000OOOO0OOOOOO =int (1 )#line:401
                    for O0000O0O000O0000O in range (self .data ["rows_count"]):#line:402
                        if OO0O00OO0OOOO000O [O0000O0O000O0000O ]>0 :#line:403
                            O000OOO0O0OOOO00O +=O00000OOOO0OOOOOO #line:404
                            O00000OOOO0OOOOOO *=2 #line:405
                            O00000OOOO0OOOOOO =O00000OOOO0OOOOOO <<1 #line:406
                            print (str (O0O0OO0O00OO0OOO0 ==O000OOO0O0OOOO00O )+" @ "+str (time .time ()))#line:407
                O0OOOOO00OOO0O00O +=1 #line:408
                OOOOOOOO0OOO0000O +=1 #line:409
                if self .verbosity ['debug']:#line:410
                    print (OOO0OO0OO0OOOO000 )#line:411
            self .data ["catnames"].append (OOO0OO0OO0OOOO000 )#line:412
            self .data ["dm"].append (O0O0O000OOO00OOOO )#line:413
        print ("Encoding columns into bit-form...done")#line:415
        if self .verbosity ['hint']:#line:416
            print (f"List of attributes for analysis is: {self.data['varname']}")#line:417
            print (f"List of category names for individual attributes is : {self.data['catnames']}")#line:418
        if self .verbosity ['debug']:#line:419
            print (f"List of vtypes is (all should be 1) : {self.data['vtypes']}")#line:420
        self .data ["data_prepared"]=1 #line:421
        print ("Data preparation finished.")#line:422
        if self .verbosity ['debug']:#line:423
            print ('Number of variables : '+str (len (self .data ["dm"])))#line:424
            print ('Total number of categories in all variables : '+str (OOOOOOOO0OOO0000O ))#line:425
        self .stats ['end_prep_time']=time .time ()#line:426
        if self .verbosity ['debug']:#line:427
            print ('Time needed for data preparation : ',str (self .stats ['end_prep_time']-self .stats ['start_prep_time']))#line:428
    def _bitcount (self ,n ):#line:430
        O00OO000O0OOOOOO0 =None #line:431
        if (self ._is_py310 ):#line:432
            O00OO000O0OOOOOO0 =n .bit_count ()#line:433
        else :#line:434
            O00OO000O0OOOOOO0 =bin (n ).count ("1")#line:435
        return O00OO000O0OOOOOO0 #line:436
    def _verifyCF (self ,_cond ):#line:439
        O0O0000000O0O0O00 =self ._bitcount (_cond )#line:440
        O00O00O00OO0O00OO =[]#line:441
        OOO00O0O0O0OOOOOO =[]#line:442
        O00OOOOO0O0O00OOO =0 #line:443
        OOOO0OOOOO0O000OO =0 #line:444
        OOOO0O0O000O0000O =0 #line:445
        O0OO00OOOOOO00OOO =0 #line:446
        OOOO000O0O0000000 =0 #line:447
        OO0OOOO00OOOO00OO =0 #line:448
        O0OO0000OO000OOOO =0 #line:449
        O0OO000OO00OOO00O =0 #line:450
        OO0O0O000O0OO0OOO =0 #line:451
        OOO0O0O0O0O0O000O =None #line:452
        O00O0O0OO00O000OO =None #line:453
        O0000O0O000O0O0OO =None #line:454
        if ('min_step_size'in self .quantifiers ):#line:455
            OOO0O0O0O0O0O000O =self .quantifiers .get ('min_step_size')#line:456
        if ('min_rel_step_size'in self .quantifiers ):#line:457
            O00O0O0OO00O000OO =self .quantifiers .get ('min_rel_step_size')#line:458
            if O00O0O0OO00O000OO >=1 and O00O0O0OO00O000OO <100 :#line:459
                O00O0O0OO00O000OO =O00O0O0OO00O000OO /100 #line:460
        OO00O0O0OOOOOO000 =0 #line:461
        O000O00O0O0O00000 =0 #line:462
        O0OO00OOO00O00O00 =[]#line:463
        if ('aad_weights'in self .quantifiers ):#line:464
            OO00O0O0OOOOOO000 =1 #line:465
            OOO0O00OOO0O0OO00 =[]#line:466
            O0OO00OOO00O00O00 =self .quantifiers .get ('aad_weights')#line:467
        OO0000000000O0OO0 =self .data ["dm"][self .data ["varname"].index (self .kwargs .get ('target'))]#line:468
        def O000000OO000OO00O (act ,last ):#line:469
            OO0OOO0O000OO00OO =True #line:470
            if (act >last ):#line:471
                if not (OOO0O0O0O0O0O000O is None or act >=last +OOO0O0O0O0O0O000O ):#line:472
                    OO0OOO0O000OO00OO =False #line:473
                if not (O00O0O0OO00O000OO is None or act >=last *(1 +O00O0O0OO00O000OO )):#line:474
                    OO0OOO0O000OO00OO =False #line:475
            if (act <last ):#line:476
                if not (OOO0O0O0O0O0O000O is None or act <=last -OOO0O0O0O0O0O000O ):#line:477
                    OO0OOO0O000OO00OO =False #line:478
                if not (O00O0O0OO00O000OO is None or act <=last *(1 -O00O0O0OO00O000OO )):#line:479
                    OO0OOO0O000OO00OO =False #line:480
            return OO0OOO0O000OO00OO #line:481
        for OO00000OO0OOOO00O in range (len (OO0000000000O0OO0 )):#line:482
            OOOO0OOOOO0O000OO =O00OOOOO0O0O00OOO #line:484
            O00OOOOO0O0O00OOO =self ._bitcount (_cond &OO0000000000O0OO0 [OO00000OO0OOOO00O ])#line:485
            O00O00O00OO0O00OO .append (O00OOOOO0O0O00OOO )#line:486
            if OO00000OO0OOOO00O >0 :#line:487
                if (O00OOOOO0O0O00OOO >OOOO0OOOOO0O000OO ):#line:488
                    if (OOOO0O0O000O0000O ==1 )and (O000000OO000OO00O (O00OOOOO0O0O00OOO ,OOOO0OOOOO0O000OO )):#line:489
                        O0OO000OO00OOO00O +=1 #line:490
                    else :#line:491
                        if O000000OO000OO00O (O00OOOOO0O0O00OOO ,OOOO0OOOOO0O000OO ):#line:492
                            O0OO000OO00OOO00O =1 #line:493
                        else :#line:494
                            O0OO000OO00OOO00O =0 #line:495
                    if O0OO000OO00OOO00O >O0OO00OOOOOO00OOO :#line:496
                        O0OO00OOOOOO00OOO =O0OO000OO00OOO00O #line:497
                    OOOO0O0O000O0000O =1 #line:498
                    if O000000OO000OO00O (O00OOOOO0O0O00OOO ,OOOO0OOOOO0O000OO ):#line:499
                        OO0OOOO00OOOO00OO +=1 #line:500
                if (O00OOOOO0O0O00OOO <OOOO0OOOOO0O000OO ):#line:501
                    if (OOOO0O0O000O0000O ==-1 )and (O000000OO000OO00O (O00OOOOO0O0O00OOO ,OOOO0OOOOO0O000OO )):#line:502
                        OO0O0O000O0OO0OOO +=1 #line:503
                    else :#line:504
                        if O000000OO000OO00O (O00OOOOO0O0O00OOO ,OOOO0OOOOO0O000OO ):#line:505
                            OO0O0O000O0OO0OOO =1 #line:506
                        else :#line:507
                            OO0O0O000O0OO0OOO =0 #line:508
                    if OO0O0O000O0OO0OOO >OOOO000O0O0000000 :#line:509
                        OOOO000O0O0000000 =OO0O0O000O0OO0OOO #line:510
                    OOOO0O0O000O0000O =-1 #line:511
                    if O000000OO000OO00O (O00OOOOO0O0O00OOO ,OOOO0OOOOO0O000OO ):#line:512
                        O0OO0000OO000OOOO +=1 #line:513
                if (O00OOOOO0O0O00OOO ==OOOO0OOOOO0O000OO ):#line:514
                    OOOO0O0O000O0000O =0 #line:515
                    OO0O0O000O0OO0OOO =0 #line:516
                    O0OO000OO00OOO00O =0 #line:517
            if (OO00O0O0OOOOOO000 ):#line:519
                OOOOO00O0OO00O0OO =self ._bitcount (OO0000000000O0OO0 [OO00000OO0OOOO00O ])#line:520
                OOO0O00OOO0O0OO00 .append (OOOOO00O0OO00O0OO )#line:521
        if (OO00O0O0OOOOOO000 &sum (O00O00O00OO0O00OO )>0 ):#line:523
            for OO00000OO0OOOO00O in range (len (OO0000000000O0OO0 )):#line:524
                if OOO0O00OOO0O0OO00 [OO00000OO0OOOO00O ]>0 :#line:525
                    if O00O00O00OO0O00OO [OO00000OO0OOOO00O ]/sum (O00O00O00OO0O00OO )>OOO0O00OOO0O0OO00 [OO00000OO0OOOO00O ]/sum (OOO0O00OOO0O0OO00 ):#line:526
                        O000O00O0O0O00000 +=O0OO00OOO00O00O00 [OO00000OO0OOOO00O ]*((O00O00O00OO0O00OO [OO00000OO0OOOO00O ]/sum (O00O00O00OO0O00OO ))/(OOO0O00OOO0O0OO00 [OO00000OO0OOOO00O ]/sum (OOO0O00OOO0O0OO00 ))-1 )#line:527
        OO0O0OOO0O00OOOO0 =True #line:530
        for O0OOOOOOO00O000OO in self .quantifiers .keys ():#line:531
            if O0OOOOOOO00O000OO .upper ()=='BASE':#line:532
                OO0O0OOO0O00OOOO0 =OO0O0OOO0O00OOOO0 and (self .quantifiers .get (O0OOOOOOO00O000OO )<=O0O0000000O0O0O00 )#line:533
            if O0OOOOOOO00O000OO .upper ()=='RELBASE':#line:534
                OO0O0OOO0O00OOOO0 =OO0O0OOO0O00OOOO0 and (self .quantifiers .get (O0OOOOOOO00O000OO )<=O0O0000000O0O0O00 *1.0 /self .data ["rows_count"])#line:535
            if O0OOOOOOO00O000OO .upper ()=='S_UP':#line:536
                OO0O0OOO0O00OOOO0 =OO0O0OOO0O00OOOO0 and (self .quantifiers .get (O0OOOOOOO00O000OO )<=O0OO00OOOOOO00OOO )#line:537
            if O0OOOOOOO00O000OO .upper ()=='S_DOWN':#line:538
                OO0O0OOO0O00OOOO0 =OO0O0OOO0O00OOOO0 and (self .quantifiers .get (O0OOOOOOO00O000OO )<=OOOO000O0O0000000 )#line:539
            if O0OOOOOOO00O000OO .upper ()=='S_ANY_UP':#line:540
                OO0O0OOO0O00OOOO0 =OO0O0OOO0O00OOOO0 and (self .quantifiers .get (O0OOOOOOO00O000OO )<=O0OO00OOOOOO00OOO )#line:541
            if O0OOOOOOO00O000OO .upper ()=='S_ANY_DOWN':#line:542
                OO0O0OOO0O00OOOO0 =OO0O0OOO0O00OOOO0 and (self .quantifiers .get (O0OOOOOOO00O000OO )<=OOOO000O0O0000000 )#line:543
            if O0OOOOOOO00O000OO .upper ()=='MAX':#line:544
                OO0O0OOO0O00OOOO0 =OO0O0OOO0O00OOOO0 and (self .quantifiers .get (O0OOOOOOO00O000OO )<=max (O00O00O00OO0O00OO ))#line:545
            if O0OOOOOOO00O000OO .upper ()=='MIN':#line:546
                OO0O0OOO0O00OOOO0 =OO0O0OOO0O00OOOO0 and (self .quantifiers .get (O0OOOOOOO00O000OO )<=min (O00O00O00OO0O00OO ))#line:547
            if O0OOOOOOO00O000OO .upper ()=='RELMAX':#line:548
                if sum (O00O00O00OO0O00OO )>0 :#line:549
                    OO0O0OOO0O00OOOO0 =OO0O0OOO0O00OOOO0 and (self .quantifiers .get (O0OOOOOOO00O000OO )<=max (O00O00O00OO0O00OO )*1.0 /sum (O00O00O00OO0O00OO ))#line:550
                else :#line:551
                    OO0O0OOO0O00OOOO0 =False #line:552
            if O0OOOOOOO00O000OO .upper ()=='RELMAX_LEQ':#line:553
                if sum (O00O00O00OO0O00OO )>0 :#line:554
                    OO0O0OOO0O00OOOO0 =OO0O0OOO0O00OOOO0 and (self .quantifiers .get (O0OOOOOOO00O000OO )>=max (O00O00O00OO0O00OO )*1.0 /sum (O00O00O00OO0O00OO ))#line:555
                else :#line:556
                    OO0O0OOO0O00OOOO0 =False #line:557
            if O0OOOOOOO00O000OO .upper ()=='RELMIN':#line:558
                if sum (O00O00O00OO0O00OO )>0 :#line:559
                    OO0O0OOO0O00OOOO0 =OO0O0OOO0O00OOOO0 and (self .quantifiers .get (O0OOOOOOO00O000OO )<=min (O00O00O00OO0O00OO )*1.0 /sum (O00O00O00OO0O00OO ))#line:560
                else :#line:561
                    OO0O0OOO0O00OOOO0 =False #line:562
            if O0OOOOOOO00O000OO .upper ()=='RELMIN_LEQ':#line:563
                if sum (O00O00O00OO0O00OO )>0 :#line:564
                    OO0O0OOO0O00OOOO0 =OO0O0OOO0O00OOOO0 and (self .quantifiers .get (O0OOOOOOO00O000OO )>=min (O00O00O00OO0O00OO )*1.0 /sum (O00O00O00OO0O00OO ))#line:565
                else :#line:566
                    OO0O0OOO0O00OOOO0 =False #line:567
            if O0OOOOOOO00O000OO .upper ()=='AAD':#line:568
                OO0O0OOO0O00OOOO0 =OO0O0OOO0O00OOOO0 and (self .quantifiers .get (O0OOOOOOO00O000OO )<=O000O00O0O0O00000 )#line:569
            if O0OOOOOOO00O000OO .upper ()=='RELRANGE_LEQ':#line:570
                O00OO0O0OOO00OOO0 =self .quantifiers .get (O0OOOOOOO00O000OO )#line:571
                if O00OO0O0OOO00OOO0 >=1 and O00OO0O0OOO00OOO0 <100 :#line:572
                    O00OO0O0OOO00OOO0 =O00OO0O0OOO00OOO0 *1.0 /100 #line:573
                O0O0O00000O000000 =min (O00O00O00OO0O00OO )*1.0 /sum (O00O00O00OO0O00OO )#line:574
                OOO0OOOOOOOOO00OO =max (O00O00O00OO0O00OO )*1.0 /sum (O00O00O00OO0O00OO )#line:575
                OO0O0OOO0O00OOOO0 =OO0O0OOO0O00OOOO0 and (O00OO0O0OOO00OOO0 >=OOO0OOOOOOOOO00OO -O0O0O00000O000000 )#line:576
        OO000OO0OO000OOO0 ={}#line:577
        if OO0O0OOO0O00OOOO0 ==True :#line:578
            if self .verbosity ['debug']:#line:579
                print ("Rule found: base: "+str (O0O0000000O0O0O00 )+", hist: "+str (O00O00O00OO0O00OO )+", max: "+str (max (O00O00O00OO0O00OO ))+", min: "+str (min (O00O00O00OO0O00OO ))+", s_up: "+str (O0OO00OOOOOO00OOO )+", s_down: "+str (OOOO000O0O0000000 ))#line:580
            self .stats ['total_valid']+=1 #line:581
            OO000OO0OO000OOO0 ["base"]=O0O0000000O0O0O00 #line:582
            OO000OO0OO000OOO0 ["rel_base"]=O0O0000000O0O0O00 *1.0 /self .data ["rows_count"]#line:583
            OO000OO0OO000OOO0 ["s_up"]=O0OO00OOOOOO00OOO #line:584
            OO000OO0OO000OOO0 ["s_down"]=OOOO000O0O0000000 #line:585
            OO000OO0OO000OOO0 ["s_any_up"]=OO0OOOO00OOOO00OO #line:586
            OO000OO0OO000OOO0 ["s_any_down"]=O0OO0000OO000OOOO #line:587
            OO000OO0OO000OOO0 ["max"]=max (O00O00O00OO0O00OO )#line:588
            OO000OO0OO000OOO0 ["min"]=min (O00O00O00OO0O00OO )#line:589
            if self .verbosity ['debug']:#line:590
                OO000OO0OO000OOO0 ["rel_max"]=max (O00O00O00OO0O00OO )*1.0 /self .data ["rows_count"]#line:591
                OO000OO0OO000OOO0 ["rel_min"]=min (O00O00O00OO0O00OO )*1.0 /self .data ["rows_count"]#line:592
            if sum (O00O00O00OO0O00OO )>0 :#line:593
                OO000OO0OO000OOO0 ["rel_max"]=max (O00O00O00OO0O00OO )*1.0 /sum (O00O00O00OO0O00OO )#line:594
                OO000OO0OO000OOO0 ["rel_min"]=min (O00O00O00OO0O00OO )*1.0 /sum (O00O00O00OO0O00OO )#line:595
            else :#line:596
                OO000OO0OO000OOO0 ["rel_max"]=0 #line:597
                OO000OO0OO000OOO0 ["rel_min"]=0 #line:598
            OO000OO0OO000OOO0 ["hist"]=O00O00O00OO0O00OO #line:599
            if OO00O0O0OOOOOO000 :#line:600
                OO000OO0OO000OOO0 ["aad"]=O000O00O0O0O00000 #line:601
                OO000OO0OO000OOO0 ["hist_full"]=OOO0O00OOO0O0OO00 #line:602
                OO000OO0OO000OOO0 ["rel_hist"]=[OO0OO0O00O00O0O00 /sum (O00O00O00OO0O00OO )for OO0OO0O00O00O0O00 in O00O00O00OO0O00OO ]#line:603
                OO000OO0OO000OOO0 ["rel_hist_full"]=[OO0OO0OOO00OOO000 /sum (OOO0O00OOO0O0OO00 )for OO0OO0OOO00OOO000 in OOO0O00OOO0O0OO00 ]#line:604
        if self .verbosity ['debug']:#line:605
            print ("Info: base: "+str (O0O0000000O0O0O00 )+", hist: "+str (O00O00O00OO0O00OO )+", max: "+str (max (O00O00O00OO0O00OO ))+", min: "+str (min (O00O00O00OO0O00OO ))+", s_up: "+str (O0OO00OOOOOO00OOO )+", s_down: "+str (OOOO000O0O0000000 ))#line:606
        return OO0O0OOO0O00OOOO0 ,OO000OO0OO000OOO0 #line:607
    def _verifyUIC (self ,_cond ):#line:609
        OO00000OO0OO00O00 ={}#line:610
        OO00OOOO0OO0OO0O0 =0 #line:611
        for OO00000OO0OOO0O0O in self .task_actinfo ['cedents']:#line:612
            OO00000OO0OO00O00 [OO00000OO0OOO0O0O ['cedent_type']]=OO00000OO0OOO0O0O ['filter_value']#line:613
            OO00OOOO0OO0OO0O0 =OO00OOOO0OO0OO0O0 +1 #line:614
        if self .verbosity ['debug']:#line:615
            print (OO00000OO0OOO0O0O ['cedent_type']+" : "+str (OO00000OO0OOO0O0O ['filter_value']))#line:616
        O0OO00OOOO0OOOOO0 =self ._bitcount (_cond )#line:617
        OO00OOO0OOO000OO0 =[]#line:618
        O0000OO0OO00OOOOO =0 #line:619
        O0000O0OOO0OO0000 =0 #line:620
        O000OO000OO0O000O =0 #line:621
        OO00OOOO0OOO0O0O0 =[]#line:622
        O0OOO00O00O0OOOOO =[]#line:623
        if ('aad_weights'in self .quantifiers ):#line:624
            OO00OOOO0OOO0O0O0 =self .quantifiers .get ('aad_weights')#line:625
            O0000O0OOO0OO0000 =1 #line:626
        O000O0OOO00O0OOO0 =self .data ["dm"][self .data ["varname"].index (self .kwargs .get ('target'))]#line:627
        for OOO0OOO000OOO00O0 in range (len (O000O0OOO00O0OOO0 )):#line:628
            O00OOO0O0OO0O00OO =O0000OO0OO00OOOOO #line:630
            O0000OO0OO00OOOOO =self ._bitcount (_cond &O000O0OOO00O0OOO0 [OOO0OOO000OOO00O0 ])#line:631
            OO00OOO0OOO000OO0 .append (O0000OO0OO00OOOOO )#line:632
            OOOOO0O00OO0OOOOO =self ._bitcount (OO00000OO0OO00O00 ['cond']&O000O0OOO00O0OOO0 [OOO0OOO000OOO00O0 ])#line:634
            O0OOO00O00O0OOOOO .append (OOOOO0O00OO0OOOOO )#line:635
        O000OOOO0OO0O00OO =0 #line:637
        O0OO0O000OOOO0O00 =0 #line:638
        if (O0000O0OOO0OO0000 &sum (OO00OOO0OOO000OO0 )>0 ):#line:639
            for OOO0OOO000OOO00O0 in range (len (O000O0OOO00O0OOO0 )):#line:640
                if O0OOO00O00O0OOOOO [OOO0OOO000OOO00O0 ]>0 :#line:641
                    if OO00OOO0OOO000OO0 [OOO0OOO000OOO00O0 ]/sum (OO00OOO0OOO000OO0 )>O0OOO00O00O0OOOOO [OOO0OOO000OOO00O0 ]/sum (O0OOO00O00O0OOOOO ):#line:642
                        O000OO000OO0O000O +=OO00OOOO0OOO0O0O0 [OOO0OOO000OOO00O0 ]*((OO00OOO0OOO000OO0 [OOO0OOO000OOO00O0 ]/sum (OO00OOO0OOO000OO0 ))/(O0OOO00O00O0OOOOO [OOO0OOO000OOO00O0 ]/sum (O0OOO00O00O0OOOOO ))-1 )#line:643
                if OO00OOOO0OOO0O0O0 [OOO0OOO000OOO00O0 ]>0 :#line:644
                    O000OOOO0OO0O00OO +=OO00OOO0OOO000OO0 [OOO0OOO000OOO00O0 ]#line:645
                    O0OO0O000OOOO0O00 +=O0OOO00O00O0OOOOO [OOO0OOO000OOO00O0 ]#line:646
        O00O0OOOOOO000OO0 =0 #line:647
        if sum (OO00OOO0OOO000OO0 )>0 and O0OO0O000OOOO0O00 >0 :#line:648
            O00O0OOOOOO000OO0 =(O000OOOO0OO0O00OO /sum (OO00OOO0OOO000OO0 ))/(O0OO0O000OOOO0O00 /sum (O0OOO00O00O0OOOOO ))#line:649
        OO000OO00OO00OO00 =True #line:653
        for OO00OOO000O0O0O0O in self .quantifiers .keys ():#line:654
            if OO00OOO000O0O0O0O .upper ()=='BASE':#line:655
                OO000OO00OO00OO00 =OO000OO00OO00OO00 and (self .quantifiers .get (OO00OOO000O0O0O0O )<=O0OO00OOOO0OOOOO0 )#line:656
            if OO00OOO000O0O0O0O .upper ()=='RELBASE':#line:657
                OO000OO00OO00OO00 =OO000OO00OO00OO00 and (self .quantifiers .get (OO00OOO000O0O0O0O )<=O0OO00OOOO0OOOOO0 *1.0 /self .data ["rows_count"])#line:658
            if OO00OOO000O0O0O0O .upper ()=='AAD_SCORE':#line:659
                OO000OO00OO00OO00 =OO000OO00OO00OO00 and (self .quantifiers .get (OO00OOO000O0O0O0O )<=O000OO000OO0O000O )#line:660
            if OO00OOO000O0O0O0O .upper ()=='RELEVANT_CAT_BASE':#line:661
                OO000OO00OO00OO00 =OO000OO00OO00OO00 and (self .quantifiers .get (OO00OOO000O0O0O0O )<=O000OOOO0OO0O00OO )#line:662
            if OO00OOO000O0O0O0O .upper ()=='RELEVANT_BASE_LIFT':#line:663
                OO000OO00OO00OO00 =OO000OO00OO00OO00 and (self .quantifiers .get (OO00OOO000O0O0O0O )<=O00O0OOOOOO000OO0 )#line:664
        OOOOOOO0O0O00O0OO ={}#line:665
        if OO000OO00OO00OO00 ==True :#line:666
            self .stats ['total_valid']+=1 #line:667
            OOOOOOO0O0O00O0OO ["base"]=O0OO00OOOO0OOOOO0 #line:668
            OOOOOOO0O0O00O0OO ["rel_base"]=O0OO00OOOO0OOOOO0 *1.0 /self .data ["rows_count"]#line:669
            OOOOOOO0O0O00O0OO ["hist"]=OO00OOO0OOO000OO0 #line:670
            OOOOOOO0O0O00O0OO ["aad_score"]=O000OO000OO0O000O #line:671
            OOOOOOO0O0O00O0OO ["hist_cond"]=O0OOO00O00O0OOOOO #line:672
            OOOOOOO0O0O00O0OO ["rel_hist"]=[OO000OOOO0O00OOO0 /sum (OO00OOO0OOO000OO0 )for OO000OOOO0O00OOO0 in OO00OOO0OOO000OO0 ]#line:673
            OOOOOOO0O0O00O0OO ["rel_hist_cond"]=[OOOO0OOOO000OOO00 /sum (O0OOO00O00O0OOOOO )for OOOO0OOOO000OOO00 in O0OOO00O00O0OOOOO ]#line:674
            OOOOOOO0O0O00O0OO ["relevant_base_lift"]=O00O0OOOOOO000OO0 #line:675
            OOOOOOO0O0O00O0OO ["relevant_cat_base"]=O000OOOO0OO0O00OO #line:676
            OOOOOOO0O0O00O0OO ["relevant_cat_base_full"]=O0OO0O000OOOO0O00 #line:677
        return OO000OO00OO00OO00 ,OOOOOOO0O0O00O0OO #line:678
    def _verify4ft (self ,_cond ,_trace_cedent =None ,_traces =None ):#line:680
        OOOO00O000OO0O000 ={}#line:681
        OOOOOO00000OO00O0 =0 #line:682
        for O000OOOO00O00000O in self .task_actinfo ['cedents']:#line:683
            OOOO00O000OO0O000 [O000OOOO00O00000O ['cedent_type']]=O000OOOO00O00000O ['filter_value']#line:684
            OOOOOO00000OO00O0 =OOOOOO00000OO00O0 +1 #line:685
        O000OO000O0O00OO0 =self ._bitcount (OOOO00O000OO0O000 ['ante']&OOOO00O000OO0O000 ['succ']&OOOO00O000OO0O000 ['cond'])#line:686
        OOOO0O00O0000OO0O =None #line:687
        OOOO0O00O0000OO0O =0 #line:688
        if O000OO000O0O00OO0 >0 :#line:689
            OOOO0O00O0000OO0O =self ._bitcount (OOOO00O000OO0O000 ['ante']&OOOO00O000OO0O000 ['succ']&OOOO00O000OO0O000 ['cond'])*1.0 /self ._bitcount (OOOO00O000OO0O000 ['ante']&OOOO00O000OO0O000 ['cond'])#line:690
        O000OO0OOOOO000OO =1 <<self .data ["rows_count"]#line:692
        OOOO0O0O0OOO000OO =self ._bitcount (OOOO00O000OO0O000 ['ante']&OOOO00O000OO0O000 ['succ']&OOOO00O000OO0O000 ['cond'])#line:693
        OO000OOOO000O00OO =self ._bitcount (OOOO00O000OO0O000 ['ante']&~(O000OO0OOOOO000OO |OOOO00O000OO0O000 ['succ'])&OOOO00O000OO0O000 ['cond'])#line:694
        O000OOOO00O00000O =self ._bitcount (~(O000OO0OOOOO000OO |OOOO00O000OO0O000 ['ante'])&OOOO00O000OO0O000 ['succ']&OOOO00O000OO0O000 ['cond'])#line:695
        OOOO0O0OOO0OOO00O =self ._bitcount (~(O000OO0OOOOO000OO |OOOO00O000OO0O000 ['ante'])&~(O000OO0OOOOO000OO |OOOO00O000OO0O000 ['succ'])&OOOO00O000OO0O000 ['cond'])#line:696
        OO0O000OOO00OO000 =0 #line:697
        OO0000O0OOOOO0O00 =0 #line:698
        if (OOOO0O0O0OOO000OO +OO000OOOO000O00OO )*(OOOO0O0O0OOO000OO +O000OOOO00O00000O )>0 :#line:699
            OO0O000OOO00OO000 =OOOO0O0O0OOO000OO *(OOOO0O0O0OOO000OO +OO000OOOO000O00OO +O000OOOO00O00000O +OOOO0O0OOO0OOO00O )/(OOOO0O0O0OOO000OO +OO000OOOO000O00OO )/(OOOO0O0O0OOO000OO +O000OOOO00O00000O )-1 #line:700
            OO0000O0OOOOO0O00 =OO0O000OOO00OO000 +1 #line:701
        else :#line:702
            OO0O000OOO00OO000 =None #line:703
            OO0000O0OOOOO0O00 =None #line:704
        OO00OOOOO0O0OOO00 =0 #line:705
        if (OOOO0O0O0OOO000OO +OO000OOOO000O00OO )*(OOOO0O0O0OOO000OO +O000OOOO00O00000O )>0 :#line:706
            OO00OOOOO0O0OOO00 =1 -OOOO0O0O0OOO000OO *(OOOO0O0O0OOO000OO +OO000OOOO000O00OO +O000OOOO00O00000O +OOOO0O0OOO0OOO00O )/(OOOO0O0O0OOO000OO +OO000OOOO000O00OO )/(OOOO0O0O0OOO000OO +O000OOOO00O00000O )#line:707
        else :#line:708
            OO00OOOOO0O0OOO00 =None #line:709
        OO0OO000000000000 =True #line:710
        for O0000OOOO0OO0OOO0 in self .quantifiers .keys ():#line:711
            if O0000OOOO0OO0OOO0 .upper ()=='BASE':#line:712
                OO0OO000000000000 =OO0OO000000000000 and (self .quantifiers .get (O0000OOOO0OO0OOO0 )<=O000OO000O0O00OO0 )#line:713
            if O0000OOOO0OO0OOO0 .upper ()=='RELBASE':#line:714
                OO0OO000000000000 =OO0OO000000000000 and (self .quantifiers .get (O0000OOOO0OO0OOO0 )<=O000OO000O0O00OO0 *1.0 /self .data ["rows_count"])#line:715
            if (O0000OOOO0OO0OOO0 .upper ()=='PIM')or (O0000OOOO0OO0OOO0 .upper ()=='CONF'):#line:716
                OO0OO000000000000 =OO0OO000000000000 and (self .quantifiers .get (O0000OOOO0OO0OOO0 )<=OOOO0O00O0000OO0O )#line:717
            if O0000OOOO0OO0OOO0 .upper ()=='AAD':#line:718
                if OO0O000OOO00OO000 !=None :#line:719
                    OO0OO000000000000 =OO0OO000000000000 and (self .quantifiers .get (O0000OOOO0OO0OOO0 )<=OO0O000OOO00OO000 )#line:720
                else :#line:721
                    OO0OO000000000000 =False #line:722
            if O0000OOOO0OO0OOO0 .upper ()=='BAD':#line:723
                if OO00OOOOO0O0OOO00 !=None :#line:724
                    OO0OO000000000000 =OO0OO000000000000 and (self .quantifiers .get (O0000OOOO0OO0OOO0 )<=OO00OOOOO0O0OOO00 )#line:725
                else :#line:726
                    OO0OO000000000000 =False #line:727
            if O0000OOOO0OO0OOO0 .upper ()=='LAMBDA'or O0000OOOO0OO0OOO0 .upper ()=='FN':#line:728
                O00OOOOOOO0OOO000 =self .quantifiers .get (O0000OOOO0OO0OOO0 )#line:729
                OO000OOOOO0000OO0 =[OOOO0O0O0OOO000OO ,OO000OOOO000O00OO ,O000OOOO00O00000O ,OOOO0O0OOO0OOO00O ]#line:730
                OOOOOOOO00O0OOO0O =O00OOOOOOO0OOO000 .__code__ .co_argcount #line:731
                if OOOOOOOO00O0OOO0O ==1 :#line:733
                    OO0OO000000000000 =OO0OO000000000000 and O00OOOOOOO0OOO000 (OO000OOOOO0000OO0 )#line:734
                elif OOOOOOOO00O0OOO0O ==2 :#line:735
                    OO0OO0OO0O0O00O00 ={}#line:736
                    O0O00O00000O00OO0 ={}#line:737
                    O0O00O00000O00OO0 ["varname"]=self .data ["varname"]#line:738
                    O0O00O00000O00OO0 ["catnames"]=self .data ["catnames"]#line:739
                    OO0OO0OO0O0O00O00 ['datalabels']=O0O00O00000O00OO0 #line:740
                    OO0OO0OO0O0O00O00 ['trace_cedent']=_trace_cedent #line:741
                    OO0OO0OO0O0O00O00 ['traces']=_traces #line:742
                    OO0OO000000000000 =OO0OO000000000000 and O00OOOOOOO0OOO000 (OO000OOOOO0000OO0 ,OO0OO0OO0O0O00O00 )#line:745
                else :#line:746
                    print (f"Unsupported number of arguments for lambda function ({OOOOOOOO00O0OOO0O} for procedure SD4ft-Miner")#line:747
            OO00OO0OOOOO00OO0 ={}#line:748
        if OO0OO000000000000 ==True :#line:749
            self .stats ['total_valid']+=1 #line:750
            OO00OO0OOOOO00OO0 ["base"]=O000OO000O0O00OO0 #line:751
            OO00OO0OOOOO00OO0 ["rel_base"]=O000OO000O0O00OO0 *1.0 /self .data ["rows_count"]#line:752
            OO00OO0OOOOO00OO0 ["conf"]=OOOO0O00O0000OO0O #line:753
            OO00OO0OOOOO00OO0 ["aad"]=OO0O000OOO00OO000 #line:754
            OO00OO0OOOOO00OO0 ["bad"]=OO00OOOOO0O0OOO00 #line:755
            OO00OO0OOOOO00OO0 ["fourfold"]=[OOOO0O0O0OOO000OO ,OO000OOOO000O00OO ,O000OOOO00O00000O ,OOOO0O0OOO0OOO00O ]#line:756
        return OO0OO000000000000 ,OO00OO0OOOOO00OO0 #line:757
    def _verifysd4ft (self ,_cond ):#line:759
        OOO0O0O0O0OO00000 ={}#line:760
        O0OO0OO0O000OOOOO =0 #line:761
        for OO000000OO00000O0 in self .task_actinfo ['cedents']:#line:762
            OOO0O0O0O0OO00000 [OO000000OO00000O0 ['cedent_type']]=OO000000OO00000O0 ['filter_value']#line:763
            O0OO0OO0O000OOOOO =O0OO0OO0O000OOOOO +1 #line:764
        OO0O0O0OO00O0OO0O =self ._bitcount (OOO0O0O0O0OO00000 ['ante']&OOO0O0O0O0OO00000 ['succ']&OOO0O0O0O0OO00000 ['cond']&OOO0O0O0O0OO00000 ['frst'])#line:765
        O0O000O00O000OO00 =self ._bitcount (OOO0O0O0O0OO00000 ['ante']&OOO0O0O0O0OO00000 ['succ']&OOO0O0O0O0OO00000 ['cond']&OOO0O0O0O0OO00000 ['scnd'])#line:766
        O000O0O0000000OOO =None #line:767
        O0O0OOO00OOOO0000 =0 #line:768
        O0OOOO000000OOO0O =0 #line:769
        if OO0O0O0OO00O0OO0O >0 :#line:770
            O0O0OOO00OOOO0000 =self ._bitcount (OOO0O0O0O0OO00000 ['ante']&OOO0O0O0O0OO00000 ['succ']&OOO0O0O0O0OO00000 ['cond']&OOO0O0O0O0OO00000 ['frst'])*1.0 /self ._bitcount (OOO0O0O0O0OO00000 ['ante']&OOO0O0O0O0OO00000 ['cond']&OOO0O0O0O0OO00000 ['frst'])#line:771
        if O0O000O00O000OO00 >0 :#line:772
            O0OOOO000000OOO0O =self ._bitcount (OOO0O0O0O0OO00000 ['ante']&OOO0O0O0O0OO00000 ['succ']&OOO0O0O0O0OO00000 ['cond']&OOO0O0O0O0OO00000 ['scnd'])*1.0 /self ._bitcount (OOO0O0O0O0OO00000 ['ante']&OOO0O0O0O0OO00000 ['cond']&OOO0O0O0O0OO00000 ['scnd'])#line:773
        OOO0OO000O000OOOO =1 <<self .data ["rows_count"]#line:775
        O00000000OOOO0OOO =self ._bitcount (OOO0O0O0O0OO00000 ['ante']&OOO0O0O0O0OO00000 ['succ']&OOO0O0O0O0OO00000 ['cond']&OOO0O0O0O0OO00000 ['frst'])#line:776
        OO00OOO00OOO0O0OO =self ._bitcount (OOO0O0O0O0OO00000 ['ante']&~(OOO0OO000O000OOOO |OOO0O0O0O0OO00000 ['succ'])&OOO0O0O0O0OO00000 ['cond']&OOO0O0O0O0OO00000 ['frst'])#line:777
        OOOOO0OO00O000OO0 =self ._bitcount (~(OOO0OO000O000OOOO |OOO0O0O0O0OO00000 ['ante'])&OOO0O0O0O0OO00000 ['succ']&OOO0O0O0O0OO00000 ['cond']&OOO0O0O0O0OO00000 ['frst'])#line:778
        O0OOO00O0O0000OOO =self ._bitcount (~(OOO0OO000O000OOOO |OOO0O0O0O0OO00000 ['ante'])&~(OOO0OO000O000OOOO |OOO0O0O0O0OO00000 ['succ'])&OOO0O0O0O0OO00000 ['cond']&OOO0O0O0O0OO00000 ['frst'])#line:779
        O000O0OOO0O00OOO0 =self ._bitcount (OOO0O0O0O0OO00000 ['ante']&OOO0O0O0O0OO00000 ['succ']&OOO0O0O0O0OO00000 ['cond']&OOO0O0O0O0OO00000 ['scnd'])#line:780
        OO0OOOO00OO0OO000 =self ._bitcount (OOO0O0O0O0OO00000 ['ante']&~(OOO0OO000O000OOOO |OOO0O0O0O0OO00000 ['succ'])&OOO0O0O0O0OO00000 ['cond']&OOO0O0O0O0OO00000 ['scnd'])#line:781
        OO0O000OOOO000000 =self ._bitcount (~(OOO0OO000O000OOOO |OOO0O0O0O0OO00000 ['ante'])&OOO0O0O0O0OO00000 ['succ']&OOO0O0O0O0OO00000 ['cond']&OOO0O0O0O0OO00000 ['scnd'])#line:782
        OO0O0OO00O00OO000 =self ._bitcount (~(OOO0OO000O000OOOO |OOO0O0O0O0OO00000 ['ante'])&~(OOO0OO000O000OOOO |OOO0O0O0O0OO00000 ['succ'])&OOO0O0O0O0OO00000 ['cond']&OOO0O0O0O0OO00000 ['scnd'])#line:783
        OOOO000OOOO00OO00 =True #line:784
        for OOOO0O00OO0O00O0O in self .quantifiers .keys ():#line:785
            if (OOOO0O00OO0O00O0O .upper ()=='FRSTBASE')|(OOOO0O00OO0O00O0O .upper ()=='BASE1'):#line:786
                OOOO000OOOO00OO00 =OOOO000OOOO00OO00 and (self .quantifiers .get (OOOO0O00OO0O00O0O )<=OO0O0O0OO00O0OO0O )#line:787
            if (OOOO0O00OO0O00O0O .upper ()=='SCNDBASE')|(OOOO0O00OO0O00O0O .upper ()=='BASE2'):#line:788
                OOOO000OOOO00OO00 =OOOO000OOOO00OO00 and (self .quantifiers .get (OOOO0O00OO0O00O0O )<=O0O000O00O000OO00 )#line:789
            if (OOOO0O00OO0O00O0O .upper ()=='FRSTRELBASE')|(OOOO0O00OO0O00O0O .upper ()=='RELBASE1'):#line:790
                OOOO000OOOO00OO00 =OOOO000OOOO00OO00 and (self .quantifiers .get (OOOO0O00OO0O00O0O )<=OO0O0O0OO00O0OO0O *1.0 /self .data ["rows_count"])#line:791
            if (OOOO0O00OO0O00O0O .upper ()=='SCNDRELBASE')|(OOOO0O00OO0O00O0O .upper ()=='RELBASE2'):#line:792
                OOOO000OOOO00OO00 =OOOO000OOOO00OO00 and (self .quantifiers .get (OOOO0O00OO0O00O0O )<=O0O000O00O000OO00 *1.0 /self .data ["rows_count"])#line:793
            if (OOOO0O00OO0O00O0O .upper ()=='FRSTPIM')|(OOOO0O00OO0O00O0O .upper ()=='PIM1')|(OOOO0O00OO0O00O0O .upper ()=='FRSTCONF')|(OOOO0O00OO0O00O0O .upper ()=='CONF1'):#line:794
                OOOO000OOOO00OO00 =OOOO000OOOO00OO00 and (self .quantifiers .get (OOOO0O00OO0O00O0O )<=O0O0OOO00OOOO0000 )#line:795
            if (OOOO0O00OO0O00O0O .upper ()=='SCNDPIM')|(OOOO0O00OO0O00O0O .upper ()=='PIM2')|(OOOO0O00OO0O00O0O .upper ()=='SCNDCONF')|(OOOO0O00OO0O00O0O .upper ()=='CONF2'):#line:796
                OOOO000OOOO00OO00 =OOOO000OOOO00OO00 and (self .quantifiers .get (OOOO0O00OO0O00O0O )<=O0OOOO000000OOO0O )#line:797
            if (OOOO0O00OO0O00O0O .upper ()=='DELTAPIM')|(OOOO0O00OO0O00O0O .upper ()=='DELTACONF'):#line:798
                OOOO000OOOO00OO00 =OOOO000OOOO00OO00 and (self .quantifiers .get (OOOO0O00OO0O00O0O )<=O0O0OOO00OOOO0000 -O0OOOO000000OOO0O )#line:799
            if (OOOO0O00OO0O00O0O .upper ()=='RATIOPIM')|(OOOO0O00OO0O00O0O .upper ()=='RATIOCONF'):#line:800
                if (O0OOOO000000OOO0O >0 ):#line:801
                    OOOO000OOOO00OO00 =OOOO000OOOO00OO00 and (self .quantifiers .get (OOOO0O00OO0O00O0O )<=O0O0OOO00OOOO0000 *1.0 /O0OOOO000000OOO0O )#line:802
                else :#line:803
                    OOOO000OOOO00OO00 =False #line:804
            if (OOOO0O00OO0O00O0O .upper ()=='RATIOPIM_LEQ')|(OOOO0O00OO0O00O0O .upper ()=='RATIOCONF_LEQ'):#line:805
                if (O0OOOO000000OOO0O >0 ):#line:806
                    OOOO000OOOO00OO00 =OOOO000OOOO00OO00 and (self .quantifiers .get (OOOO0O00OO0O00O0O )>=O0O0OOO00OOOO0000 *1.0 /O0OOOO000000OOO0O )#line:807
                else :#line:808
                    OOOO000OOOO00OO00 =False #line:809
            if OOOO0O00OO0O00O0O .upper ()=='LAMBDA'or OOOO0O00OO0O00O0O .upper ()=='FN':#line:810
                OO000OOO0O0O0O00O =self .quantifiers .get (OOOO0O00OO0O00O0O )#line:811
                O00O000O000O00OO0 =OO000OOO0O0O0O00O .func_code .co_argcount #line:812
                O0OOO0O00000000OO =[O00000000OOOO0OOO ,OO00OOO00OOO0O0OO ,OOOOO0OO00O000OO0 ,O0OOO00O0O0000OOO ]#line:813
                OOO000OOOO0O0000O =[O000O0OOO0O00OOO0 ,OO0OOOO00OO0OO000 ,OO0O000OOOO000000 ,OO0O0OO00O00OO000 ]#line:814
                if O00O000O000O00OO0 ==2 :#line:815
                    OOOO000OOOO00OO00 =OOOO000OOOO00OO00 and OO000OOO0O0O0O00O (O0OOO0O00000000OO ,OOO000OOOO0O0000O )#line:816
                elif O00O000O000O00OO0 ==3 :#line:817
                    OOOO000OOOO00OO00 =OOOO000OOOO00OO00 and OO000OOO0O0O0O00O (O0OOO0O00000000OO ,OOO000OOOO0O0000O ,None )#line:818
                else :#line:819
                    print (f"Unsupported number of arguments for lambda function ({O00O000O000O00OO0} for procedure SD4ft-Miner")#line:820
        OO0O0OO00O0OO00OO ={}#line:821
        if OOOO000OOOO00OO00 ==True :#line:822
            self .stats ['total_valid']+=1 #line:823
            OO0O0OO00O0OO00OO ["base1"]=OO0O0O0OO00O0OO0O #line:824
            OO0O0OO00O0OO00OO ["base2"]=O0O000O00O000OO00 #line:825
            OO0O0OO00O0OO00OO ["rel_base1"]=OO0O0O0OO00O0OO0O *1.0 /self .data ["rows_count"]#line:826
            OO0O0OO00O0OO00OO ["rel_base2"]=O0O000O00O000OO00 *1.0 /self .data ["rows_count"]#line:827
            OO0O0OO00O0OO00OO ["conf1"]=O0O0OOO00OOOO0000 #line:828
            OO0O0OO00O0OO00OO ["conf2"]=O0OOOO000000OOO0O #line:829
            OO0O0OO00O0OO00OO ["deltaconf"]=O0O0OOO00OOOO0000 -O0OOOO000000OOO0O #line:830
            if (O0OOOO000000OOO0O >0 ):#line:831
                OO0O0OO00O0OO00OO ["ratioconf"]=O0O0OOO00OOOO0000 *1.0 /O0OOOO000000OOO0O #line:832
            else :#line:833
                OO0O0OO00O0OO00OO ["ratioconf"]=None #line:834
            OO0O0OO00O0OO00OO ["fourfold1"]=[O00000000OOOO0OOO ,OO00OOO00OOO0O0OO ,OOOOO0OO00O000OO0 ,O0OOO00O0O0000OOO ]#line:835
            OO0O0OO00O0OO00OO ["fourfold2"]=[O000O0OOO0O00OOO0 ,OO0OOOO00OO0OO000 ,OO0O000OOOO000000 ,OO0O0OO00O00OO000 ]#line:836
        return OOOO000OOOO00OO00 ,OO0O0OO00O0OO00OO #line:837
    def _verify_opt (self ,task_actinfo ,act_cedent ):#line:840
        self .stats ['total_ver']+=1 #line:841
        O000O0OOO00O0O000 =False #line:842
        if not (task_actinfo ['optim'].get ('only_con')):#line:843
            return False #line:844
        if self .verbosity ['debug']:#line:845
            print (self .options ['optimizations'])#line:846
        if not (self .options ['optimizations']):#line:847
            if self .verbosity ['debug']:#line:848
                print ("NO OPTS")#line:849
            return False #line:850
        if self .verbosity ['debug']:#line:851
            print ("OPTS")#line:852
        O0OOOO0000O0O0000 ={}#line:853
        for OOO0OO0OO0OOOO00O in self .task_actinfo ['cedents']:#line:854
            if self .verbosity ['debug']:#line:855
                print (OOO0OO0OO0OOOO00O ['cedent_type'])#line:856
            O0OOOO0000O0O0000 [OOO0OO0OO0OOOO00O ['cedent_type']]=OOO0OO0OO0OOOO00O ['filter_value']#line:857
            if self .verbosity ['debug']:#line:858
                print (OOO0OO0OO0OOOO00O ['cedent_type']+" : "+str (OOO0OO0OO0OOOO00O ['filter_value']))#line:859
        OOO0O000O0OO00O0O =1 <<self .data ["rows_count"]#line:860
        O0O00O0000O0O0000 =OOO0O000O0OO00O0O -1 #line:861
        O00O00OO0O00O0O00 =""#line:862
        O0000OO0O0OOOO00O =0 #line:863
        if (O0OOOO0000O0O0000 .get ('ante')!=None ):#line:864
            O0O00O0000O0O0000 =O0O00O0000O0O0000 &O0OOOO0000O0O0000 ['ante']#line:865
        if (O0OOOO0000O0O0000 .get ('succ')!=None ):#line:866
            O0O00O0000O0O0000 =O0O00O0000O0O0000 &O0OOOO0000O0O0000 ['succ']#line:867
        if (O0OOOO0000O0O0000 .get ('cond')!=None ):#line:868
            O0O00O0000O0O0000 =O0O00O0000O0O0000 &O0OOOO0000O0O0000 ['cond']#line:869
        OOOOO00OOO0OOOO0O =None #line:870
        if (self .proc =='CFMiner')|(self .proc =='4ftMiner')|(self .proc =='UICMiner'):#line:871
            O0OOO0000OOOO000O =self ._bitcount (O0O00O0000O0O0000 )#line:872
            if not (self ._opt_base ==None ):#line:873
                if not (self ._opt_base <=O0OOO0000OOOO000O ):#line:874
                    O000O0OOO00O0O000 =True #line:875
            if not (self ._opt_relbase ==None ):#line:876
                if not (self ._opt_relbase <=O0OOO0000OOOO000O *1.0 /self .data ["rows_count"]):#line:877
                    O000O0OOO00O0O000 =True #line:878
        if (self .proc =='SD4ftMiner'):#line:879
            O0OOO0000OOOO000O =self ._bitcount (O0O00O0000O0O0000 )#line:880
            if (not (self ._opt_base1 ==None ))&(not (self ._opt_base2 ==None )):#line:881
                if not (max (self ._opt_base1 ,self ._opt_base2 )<=O0OOO0000OOOO000O ):#line:882
                    O000O0OOO00O0O000 =True #line:883
            if (not (self ._opt_relbase1 ==None ))&(not (self ._opt_relbase2 ==None )):#line:884
                if not (max (self ._opt_relbase1 ,self ._opt_relbase2 )<=O0OOO0000OOOO000O *1.0 /self .data ["rows_count"]):#line:885
                    O000O0OOO00O0O000 =True #line:886
        return O000O0OOO00O0O000 #line:888
    def _print (self ,act_cedent ,_trace_cedent ,_traces ):#line:891
        if (len (_trace_cedent ))!=len (_traces ):#line:892
            print ("DIFF IN LEN for following cedent : "+str (len (_trace_cedent ))+" vs "+str (len (_traces )))#line:893
            print ("trace cedent : "+str (_trace_cedent )+", traces "+str (_traces ))#line:894
        OO00000OO00O00O00 =''#line:895
        O00O00OOOOOO0O0OO ={}#line:896
        OOO000O00O00000OO =[]#line:897
        for O00000OOOOOO00OO0 in range (len (_trace_cedent )):#line:898
            OOOOOOO00OOO0000O =self .data ["varname"].index (act_cedent ['defi'].get ('attributes')[_trace_cedent [O00000OOOOOO00OO0 ]].get ('name'))#line:899
            OO00000OO00O00O00 =OO00000OO00O00O00 +self .data ["varname"][OOOOOOO00OOO0000O ]+'('#line:900
            OOO000O00O00000OO .append (OOOOOOO00OOO0000O )#line:901
            O0OO0O00OO0000000 =[]#line:902
            for O000OOOOOO0O00OOO in _traces [O00000OOOOOO00OO0 ]:#line:903
                OO00000OO00O00O00 =OO00000OO00O00O00 +str (self .data ["catnames"][OOOOOOO00OOO0000O ][O000OOOOOO0O00OOO ])+" "#line:904
                O0OO0O00OO0000000 .append (str (self .data ["catnames"][OOOOOOO00OOO0000O ][O000OOOOOO0O00OOO ]))#line:905
            OO00000OO00O00O00 =OO00000OO00O00O00 [:-1 ]+')'#line:906
            O00O00OOOOOO0O0OO [self .data ["varname"][OOOOOOO00OOO0000O ]]=O0OO0O00OO0000000 #line:907
            if O00000OOOOOO00OO0 +1 <len (_trace_cedent ):#line:908
                OO00000OO00O00O00 =OO00000OO00O00O00 +' & '#line:909
        return OO00000OO00O00O00 ,O00O00OOOOOO0O0OO ,OOO000O00O00000OO #line:910
    def _print_hypo (self ,rule ):#line:912
        self .print_rule (rule )#line:913
    def _print_rule (self ,rule ):#line:915
        if self .verbosity ['print_rules']:#line:916
            print ('Rules info : '+str (rule ['params']))#line:917
            for O0OO00OOO00O00000 in self .task_actinfo ['cedents']:#line:918
                print (O0OO00OOO00O00000 ['cedent_type']+' = '+O0OO00OOO00O00000 ['generated_string'])#line:919
    def _genvar (self ,task_actinfo ,act_cedent ,_trace_cedent ,_traces ,_condc ,_minlenc ,_maxlenc ,_progress_lower ,_progress_upper ):#line:921
        _OOO00O0OOOOO0OO0O =0 #line:922
        _O0OOOOO00OO00000O =[]#line:923
        for OOOO0O00OOO00OO0O in range (act_cedent ['num_cedent']):#line:924
            if ('force'in act_cedent ['defi'].get ('attributes')[OOOO0O00OOO00OO0O ]and act_cedent ['defi'].get ('attributes')[OOOO0O00OOO00OO0O ].get ('force')):#line:926
                _O0OOOOO00OO00000O .append (OOOO0O00OOO00OO0O )#line:927
        if act_cedent ['num_cedent']>0 :#line:928
            _OOO00O0OOOOO0OO0O =(_progress_upper -_progress_lower )/act_cedent ['num_cedent']#line:929
        if act_cedent ['num_cedent']==0 :#line:930
            if len (task_actinfo ['cedents_to_do'])>len (task_actinfo ['cedents']):#line:931
                OOO000O00O0O0OOO0 ,OOOOOO00O0OOOOO00 ,O0O00O000OO0O000O =self ._print (act_cedent ,_trace_cedent ,_traces )#line:932
                act_cedent ['generated_string']=OOO000O00O0O0OOO0 #line:933
                act_cedent ['rule']=OOOOOO00O0OOOOO00 #line:934
                act_cedent ['filter_value']=(1 <<self .data ["rows_count"])-1 #line:935
                act_cedent ['traces']=[]#line:936
                act_cedent ['trace_cedent']=[]#line:937
                act_cedent ['trace_cedent_asindata']=[]#line:938
                task_actinfo ['cedents'].append (act_cedent )#line:939
                _trace_cedent .append (None )#line:940
                self ._start_cedent (task_actinfo ,_progress_lower ,_progress_upper )#line:941
                task_actinfo ['cedents'].pop ()#line:942
        for OOOO0O00OOO00OO0O in range (act_cedent ['num_cedent']):#line:945
            _O00000OO00OOO0OO0 =True #line:946
            for O000O00OOOOOOO00O in range (len (_O0OOOOO00OO00000O )):#line:947
                if O000O00OOOOOOO00O <OOOO0O00OOO00OO0O and O000O00OOOOOOO00O not in _trace_cedent and O000O00OOOOOOO00O in _O0OOOOO00OO00000O :#line:948
                    _O00000OO00OOO0OO0 =False #line:949
            if (len (_trace_cedent )==0 or OOOO0O00OOO00OO0O >_trace_cedent [-1 ])and _O00000OO00OOO0OO0 :#line:951
                _trace_cedent .append (OOOO0O00OOO00OO0O )#line:952
                OOOO0OOOOO0000OO0 =self .data ["varname"].index (act_cedent ['defi'].get ('attributes')[OOOO0O00OOO00OO0O ].get ('name'))#line:953
                _OOO000OO0OOOOOO0O =act_cedent ['defi'].get ('attributes')[OOOO0O00OOO00OO0O ].get ('minlen')#line:954
                _OOO000O00000OO00O =act_cedent ['defi'].get ('attributes')[OOOO0O00OOO00OO0O ].get ('maxlen')#line:955
                _O000000OOOOOO0OOO =act_cedent ['defi'].get ('attributes')[OOOO0O00OOO00OO0O ].get ('type')#line:956
                OO000OOO0O00O000O =len (self .data ["dm"][OOOO0OOOOO0000OO0 ])#line:957
                _O00O0O00O0OO000OO =[]#line:958
                _traces .append (_O00O0O00O0OO000OO )#line:959
                _O00O0OO0OOOOOO0OO =int (0 )#line:960
                self ._gencomb (task_actinfo ,act_cedent ,_trace_cedent ,_traces ,_O00O0O00O0OO000OO ,_condc ,_O00O0OO0OOOOOO0OO ,OO000OOO0O00O000O ,_O000000OOOOOO0OOO ,_minlenc ,_maxlenc ,_OOO000OO0OOOOOO0O ,_OOO000O00000OO00O ,_progress_lower +OOOO0O00OOO00OO0O *_OOO00O0OOOOO0OO0O ,_progress_lower +(OOOO0O00OOO00OO0O +1 )*_OOO00O0OOOOO0OO0O )#line:961
                _traces .pop ()#line:962
                _trace_cedent .pop ()#line:963
    def _gencomb (self ,task_actinfo ,act_cedent ,_trace_cedent ,_traces ,_trace ,_condc ,_cond ,attrib_count ,_type ,_minlenc ,_maxlenc ,_minlen ,_maxlen ,_progress_lower ,_progress_upper ,val_list =None ):#line:965
        _OO0OOO0000O0O000O =[]#line:966
        _O000O0O0O0O0O0O00 =val_list #line:967
        if _type =="subset":#line:968
            if len (_trace )==0 :#line:969
                _OO0OOO0000O0O000O =range (attrib_count )#line:970
            else :#line:971
                _OO0OOO0000O0O000O =range (_trace [-1 ]+1 ,attrib_count )#line:972
        elif _type =="seq":#line:973
            if len (_trace )==0 :#line:974
                _OO0OOO0000O0O000O =range (attrib_count -_minlen +1 )#line:975
            else :#line:976
                if _trace [-1 ]+1 ==attrib_count :#line:977
                    return #line:978
                OO00OOOO0OO00OO0O =_trace [-1 ]+1 #line:979
                _OO0OOO0000O0O000O .append (OO00OOOO0OO00OO0O )#line:980
        elif _type =="lcut":#line:981
            if len (_trace )==0 :#line:982
                OO00OOOO0OO00OO0O =0 ;#line:983
            else :#line:984
                if _trace [-1 ]+1 ==attrib_count :#line:985
                    return #line:986
                OO00OOOO0OO00OO0O =_trace [-1 ]+1 #line:987
            _OO0OOO0000O0O000O .append (OO00OOOO0OO00OO0O )#line:988
        elif _type =="rcut":#line:989
            if len (_trace )==0 :#line:990
                OO00OOOO0OO00OO0O =attrib_count -1 ;#line:991
            else :#line:992
                if _trace [-1 ]==0 :#line:993
                    return #line:994
                OO00OOOO0OO00OO0O =_trace [-1 ]-1 #line:995
                if self .verbosity ['debug']:#line:996
                    print ("Olditem: "+str (_trace [-1 ])+", Newitem : "+str (OO00OOOO0OO00OO0O ))#line:997
            _OO0OOO0000O0O000O .append (OO00OOOO0OO00OO0O )#line:998
        elif _type =="one":#line:999
            if len (_trace )==0 :#line:1000
                OO00O00OOO0OO00O0 =self .data ["varname"].index (act_cedent ['defi'].get ('attributes')[_trace_cedent [-1 ]].get ('name'))#line:1001
                try :#line:1002
                    OO00OOOO0OO00OO0O =self .data ["catnames"][OO00O00OOO0OO00O0 ].index (act_cedent ['defi'].get ('attributes')[_trace_cedent [-1 ]].get ('value'))#line:1003
                except :#line:1004
                    print (f"ERROR: attribute '{act_cedent['defi'].get('attributes')[_trace_cedent[-1]].get('name')}' has not value '{act_cedent['defi'].get('attributes')[_trace_cedent[-1]].get('value')}'")#line:1005
                    exit (1 )#line:1006
                _OO0OOO0000O0O000O .append (OO00OOOO0OO00OO0O )#line:1007
                _minlen =1 #line:1008
                _maxlen =1 #line:1009
            else :#line:1010
                print ("DEBUG: one category should not have more categories")#line:1011
                return #line:1012
        elif _type =="list":#line:1014
            if _O000O0O0O0O0O0O00 is None :#line:1015
                OO00O00OOO0OO00O0 =self .data ["varname"].index (act_cedent ['defi'].get ('attributes')[_trace_cedent [-1 ]].get ('name'))#line:1016
                O00OO00OOO000O0O0 =None #line:1017
                _O0O000000O0O0O00O =[]#line:1018
                try :#line:1019
                    O000O0000O0O0000O =act_cedent ['defi'].get ('attributes')[_trace_cedent [-1 ]].get ('value')#line:1020
                    for OOOOOOOOOOOOOOOOO in O000O0000O0O0000O :#line:1021
                        O00OO00OOO000O0O0 =OOOOOOOOOOOOOOOOO #line:1022
                        OO00OOOO0OO00OO0O =self .data ["catnames"][OO00O00OOO0OO00O0 ].index (OOOOOOOOOOOOOOOOO )#line:1023
                        _O0O000000O0O0O00O .append (OO00OOOO0OO00OO0O )#line:1024
                except :#line:1025
                    print (f"ERROR: attribute '{act_cedent['defi'].get('attributes')[_trace_cedent[-1]].get('name')}' has not value '{OOOOOOOOOOOOOOOOO}'")#line:1027
                    exit (1 )#line:1028
                _O000O0O0O0O0O0O00 =_O0O000000O0O0O00O #line:1029
                _minlen =len (_O000O0O0O0O0O0O00 )#line:1030
                _maxlen =len (_O000O0O0O0O0O0O00 )#line:1031
            _OO0OOO0000O0O000O .append (_O000O0O0O0O0O0O00 [len (_trace )])#line:1032
        else :#line:1034
            print ("Attribute type "+_type +" not supported.")#line:1035
            return #line:1036
        if len (_OO0OOO0000O0O000O )>0 :#line:1038
            _OOO0OO0O00O0000O0 =(_progress_upper -_progress_lower )/len (_OO0OOO0000O0O000O )#line:1039
        else :#line:1040
            _OOO0OO0O00O0000O0 =0 #line:1041
        _O0O0OOO000OOO0OOO =0 #line:1043
        for OOO000000OO00O000 in _OO0OOO0000O0O000O :#line:1045
                _trace .append (OOO000000OO00O000 )#line:1046
                _traces .pop ()#line:1047
                _traces .append (_trace )#line:1048
                _OO0000000O0000OO0 =_cond |self .data ["dm"][self .data ["varname"].index (act_cedent ['defi'].get ('attributes')[_trace_cedent [-1 ]].get ('name'))][OOO000000OO00O000 ]#line:1049
                _OO0OOO0OO00O0O000 =1 #line:1050
                if (len (_trace_cedent )<_minlenc ):#line:1051
                    _OO0OOO0OO00O0O000 =-1 #line:1052
                    if self .verbosity ['debug']:#line:1053
                        print ("DEBUG: will not verify, low cedent length")#line:1054
                if (len (_traces [-1 ])<_minlen ):#line:1055
                    _OO0OOO0OO00O0O000 =0 #line:1056
                    if self .verbosity ['debug']:#line:1057
                        print ("DEBUG: will not verify, low attribute length")#line:1058
                _OO00OO0O0OO00O00O =0 #line:1059
                if act_cedent ['defi'].get ('type')=='con':#line:1060
                    _OO00OO0O0OO00O00O =_condc &_OO0000000O0000OO0 #line:1061
                else :#line:1062
                    _OO00OO0O0OO00O00O =_condc |_OO0000000O0000OO0 #line:1063
                act_cedent ['trace_cedent']=_trace_cedent #line:1064
                act_cedent ['traces']=_traces #line:1065
                OOOOO000OO0O0OO0O ,O00O0O0O00O00O00O ,O00OO0OO0000O0OO0 =self ._print (act_cedent ,_trace_cedent ,_traces )#line:1066
                act_cedent ['generated_string']=OOOOO000OO0O0OO0O #line:1067
                act_cedent ['rule']=O00O0O0O00O00O00O #line:1068
                act_cedent ['filter_value']=_OO00OO0O0OO00O00O #line:1069
                act_cedent ['traces']=copy .deepcopy (_traces )#line:1070
                act_cedent ['trace_cedent']=copy .deepcopy (_trace_cedent )#line:1071
                act_cedent ['trace_cedent_asindata']=copy .deepcopy (O00OO0OO0000O0OO0 )#line:1072
                if self .verbosity ['debug']:#line:1073
                    print (f"TC :{act_cedent['trace_cedent_asindata']}")#line:1074
                task_actinfo ['cedents'].append (act_cedent )#line:1075
                O00OO00000O0O0OO0 =self ._verify_opt (task_actinfo ,act_cedent )#line:1076
                if self .verbosity ['debug']:#line:1077
                    print (f"DEBUG: {act_cedent['generated_string']}.")#line:1078
                    print (f"DEBUG: {_trace_cedent},{_minlenc}.")#line:1079
                    if O00OO00000O0O0OO0 :#line:1080
                        print ("DEBUG: Optimization: cutting")#line:1081
                if not (O00OO00000O0O0OO0 ):#line:1082
                    if _OO0OOO0OO00O0O000 ==1 :#line:1083
                        if self .verbosity ['debug']:#line:1084
                            print ("DEBUG: verifying")#line:1085
                        if len (task_actinfo ['cedents_to_do'])==len (task_actinfo ['cedents']):#line:1086
                            if self .proc =='CFMiner':#line:1087
                                O00OOOOOOOOO0O0O0 ,O0OOOOOO0O0O0OO0O =self ._verifyCF (_OO00OO0O0OO00O00O )#line:1088
                            elif self .proc =='UICMiner':#line:1089
                                O00OOOOOOOOO0O0O0 ,O0OOOOOO0O0O0OO0O =self ._verifyUIC (_OO00OO0O0OO00O00O )#line:1090
                            elif self .proc =='4ftMiner':#line:1091
                                O00OOOOOOOOO0O0O0 ,O0OOOOOO0O0O0OO0O =self ._verify4ft (_OO0000000O0000OO0 ,_trace_cedent ,_traces )#line:1092
                            elif self .proc =='SD4ftMiner':#line:1093
                                O00OOOOOOOOO0O0O0 ,O0OOOOOO0O0O0OO0O =self ._verifysd4ft (_OO0000000O0000OO0 )#line:1094
                            else :#line:1095
                                print ("Unsupported procedure : "+self .proc )#line:1096
                                exit (0 )#line:1097
                            if O00OOOOOOOOO0O0O0 ==True :#line:1098
                                OO0OO0O00OO0OO0OO ={}#line:1099
                                OO0OO0O00OO0OO0OO ["rule_id"]=self .stats ['total_valid']#line:1100
                                OO0OO0O00OO0OO0OO ["cedents_str"]={}#line:1101
                                OO0OO0O00OO0OO0OO ["cedents_struct"]={}#line:1102
                                OO0OO0O00OO0OO0OO ['traces']={}#line:1103
                                OO0OO0O00OO0OO0OO ['trace_cedent_taskorder']={}#line:1104
                                OO0OO0O00OO0OO0OO ['trace_cedent_dataorder']={}#line:1105
                                for OOO0000O0OOOOOOOO in task_actinfo ['cedents']:#line:1106
                                    if self .verbosity ['debug']:#line:1107
                                        print (OOO0000O0OOOOOOOO )#line:1108
                                    OO0OO0O00OO0OO0OO ['cedents_str'][OOO0000O0OOOOOOOO ['cedent_type']]=OOO0000O0OOOOOOOO ['generated_string']#line:1109
                                    OO0OO0O00OO0OO0OO ['cedents_struct'][OOO0000O0OOOOOOOO ['cedent_type']]=OOO0000O0OOOOOOOO ['rule']#line:1110
                                    OO0OO0O00OO0OO0OO ['traces'][OOO0000O0OOOOOOOO ['cedent_type']]=OOO0000O0OOOOOOOO ['traces']#line:1111
                                    OO0OO0O00OO0OO0OO ['trace_cedent_taskorder'][OOO0000O0OOOOOOOO ['cedent_type']]=OOO0000O0OOOOOOOO ['trace_cedent']#line:1112
                                    OO0OO0O00OO0OO0OO ['trace_cedent_dataorder'][OOO0000O0OOOOOOOO ['cedent_type']]=OOO0000O0OOOOOOOO ['trace_cedent_asindata']#line:1113
                                OO0OO0O00OO0OO0OO ["params"]=O0OOOOOO0O0O0OO0O #line:1114
                                if self .verbosity ['debug']:#line:1115
                                    OO0OO0O00OO0OO0OO ["trace_cedent"]=copy .deepcopy (_trace_cedent )#line:1116
                                self ._print_rule (OO0OO0O00OO0OO0OO )#line:1117
                                self .rulelist .append (OO0OO0O00OO0OO0OO )#line:1118
                            self .stats ['total_cnt']+=1 #line:1119
                            self .stats ['total_ver']+=1 #line:1120
                    if _OO0OOO0OO00O0O000 >=1 :#line:1121
                        if len (task_actinfo ['cedents_to_do'])>len (task_actinfo ['cedents']):#line:1122
                            self ._start_cedent (task_actinfo ,_progress_lower +_O0O0OOO000OOO0OOO *_OOO0OO0O00O0000O0 ,_progress_lower +(_O0O0OOO000OOO0OOO +0.33 )*_OOO0OO0O00O0000O0 )#line:1123
                    task_actinfo ['cedents'].pop ()#line:1124
                    if (not (_OO0OOO0OO00O0O000 ==0 ))and (len (_trace_cedent )<_maxlenc ):#line:1125
                        self ._genvar (task_actinfo ,act_cedent ,_trace_cedent ,_traces ,_OO00OO0O0OO00O00O ,_minlenc ,_maxlenc ,_progress_lower +(_O0O0OOO000OOO0OOO +0.33 )*_OOO0OO0O00O0000O0 ,_progress_lower +(_O0O0OOO000OOO0OOO +0.66 )*_OOO0OO0O00O0000O0 )#line:1126
                else :#line:1127
                    task_actinfo ['cedents'].pop ()#line:1128
                if len (_trace )<_maxlen :#line:1129
                    self ._gencomb (task_actinfo ,act_cedent ,_trace_cedent ,_traces ,_trace ,_condc ,_OO0000000O0000OO0 ,attrib_count ,_type ,_minlenc ,_maxlenc ,_minlen ,_maxlen ,_progress_lower +_OOO0OO0O00O0000O0 *(_O0O0OOO000OOO0OOO +0.66 ),_progress_lower +_OOO0OO0O00O0000O0 *(_O0O0OOO000OOO0OOO +1 ),_O000O0O0O0O0O0O00 )#line:1130
                _trace .pop ()#line:1131
                _O0O0OOO000OOO0OOO +=1 #line:1132
                if self .options ['progressbar']:#line:1133
                    self .bar .update (min (100 ,_progress_lower +_OOO0OO0O00O0000O0 *_O0O0OOO000OOO0OOO ))#line:1134
                if self .verbosity ['debug']:#line:1135
                    print (f"Progress : lower: {_progress_lower}, step: {_OOO0OO0O00O0000O0}, step_no: {_O0O0OOO000OOO0OOO} overall: {_progress_lower+_OOO0OO0O00O0000O0*_O0O0OOO000OOO0OOO}")#line:1136
    def _start_cedent (self ,task_actinfo ,_progress_lower ,_progress_upper ):#line:1138
        if len (task_actinfo ['cedents_to_do'])>len (task_actinfo ['cedents']):#line:1139
            _O0O0O0O0OOOOOOOO0 =[]#line:1140
            _O0OOOO000O000OOOO =[]#line:1141
            OO000OOO00O0OO0OO ={}#line:1142
            OO000OOO00O0OO0OO ['cedent_type']=task_actinfo ['cedents_to_do'][len (task_actinfo ['cedents'])]#line:1143
            O0O0O000000000O00 =OO000OOO00O0OO0OO ['cedent_type']#line:1144
            if ((O0O0O000000000O00 [-1 ]=='-')|(O0O0O000000000O00 [-1 ]=='+')):#line:1145
                O0O0O000000000O00 =O0O0O000000000O00 [:-1 ]#line:1146
            OO000OOO00O0OO0OO ['defi']=self .kwargs .get (O0O0O000000000O00 )#line:1148
            if (OO000OOO00O0OO0OO ['defi']==None ):#line:1149
                print ("Error getting cedent ",OO000OOO00O0OO0OO ['cedent_type'])#line:1150
            _OOOOO0O0000000OOO =int (0 )#line:1151
            OO000OOO00O0OO0OO ['num_cedent']=len (OO000OOO00O0OO0OO ['defi'].get ('attributes'))#line:1152
            if (OO000OOO00O0OO0OO ['defi'].get ('type')=='con'):#line:1153
                _OOOOO0O0000000OOO =(1 <<self .data ["rows_count"])-1 #line:1154
            self ._genvar (task_actinfo ,OO000OOO00O0OO0OO ,_O0O0O0O0OOOOOOOO0 ,_O0OOOO000O000OOOO ,_OOOOO0O0000000OOO ,OO000OOO00O0OO0OO ['defi'].get ('minlen'),OO000OOO00O0OO0OO ['defi'].get ('maxlen'),_progress_lower ,_progress_upper )#line:1155
    def _calc_all (self ,**OOO0OOOOOOO0O0OO0 ):#line:1158
        if "df"in OOO0OOOOOOO0O0OO0 :#line:1159
            self ._prep_data (self .kwargs .get ("df"))#line:1160
        if not (self ._initialized ):#line:1161
            print ("ERROR: dataframe is missing and not initialized with dataframe")#line:1162
        else :#line:1163
            self ._calculate (**OOO0OOOOOOO0O0OO0 )#line:1164
    def _check_cedents (self ,lst ,**O0000O000000O0OOO ):#line:1166
        OO00OO00O0000O000 =True #line:1167
        if (O0000O000000O0OOO .get ('quantifiers',None )==None ):#line:1168
            print (f"Error: missing quantifiers.")#line:1169
            OO00OO00O0000O000 =False #line:1170
            return OO00OO00O0000O000 #line:1171
        if (type (O0000O000000O0OOO .get ('quantifiers'))!=dict ):#line:1172
            print (f"Error: quantifiers are not dictionary type.")#line:1173
            OO00OO00O0000O000 =False #line:1174
            return OO00OO00O0000O000 #line:1175
        for OO0OOOOOO0O0OOO0O in lst :#line:1177
            if (O0000O000000O0OOO .get (OO0OOOOOO0O0OOO0O ,None )==None ):#line:1178
                print (f"Error: cedent {OO0OOOOOO0O0OOO0O} is missing in parameters.")#line:1179
                OO00OO00O0000O000 =False #line:1180
                return OO00OO00O0000O000 #line:1181
            OO00O00000OO00OOO =O0000O000000O0OOO .get (OO0OOOOOO0O0OOO0O )#line:1182
            if (OO00O00000OO00OOO .get ('minlen'),None )==None :#line:1183
                print (f"Error: cedent {OO0OOOOOO0O0OOO0O} has no minimal length specified.")#line:1184
                OO00OO00O0000O000 =False #line:1185
                return OO00OO00O0000O000 #line:1186
            if not (type (OO00O00000OO00OOO .get ('minlen'))is int ):#line:1187
                print (f"Error: cedent {OO0OOOOOO0O0OOO0O} has invalid type of minimal length ({type(OO00O00000OO00OOO.get('minlen'))}).")#line:1188
                OO00OO00O0000O000 =False #line:1189
                return OO00OO00O0000O000 #line:1190
            if (OO00O00000OO00OOO .get ('maxlen'),None )==None :#line:1191
                print (f"Error: cedent {OO0OOOOOO0O0OOO0O} has no maximal length specified.")#line:1192
                OO00OO00O0000O000 =False #line:1193
                return OO00OO00O0000O000 #line:1194
            if not (type (OO00O00000OO00OOO .get ('maxlen'))is int ):#line:1195
                print (f"Error: cedent {OO0OOOOOO0O0OOO0O} has invalid type of maximal length.")#line:1196
                OO00OO00O0000O000 =False #line:1197
                return OO00OO00O0000O000 #line:1198
            if (OO00O00000OO00OOO .get ('type'),None )==None :#line:1199
                print (f"Error: cedent {OO0OOOOOO0O0OOO0O} has no type specified.")#line:1200
                OO00OO00O0000O000 =False #line:1201
                return OO00OO00O0000O000 #line:1202
            if not ((OO00O00000OO00OOO .get ('type'))in (['con','dis'])):#line:1203
                print (f"Error: cedent {OO0OOOOOO0O0OOO0O} has invalid type. Allowed values are 'con' and 'dis'.")#line:1204
                OO00OO00O0000O000 =False #line:1205
                return OO00OO00O0000O000 #line:1206
            if (OO00O00000OO00OOO .get ('attributes'),None )==None :#line:1207
                print (f"Error: cedent {OO0OOOOOO0O0OOO0O} has no attributes specified.")#line:1208
                OO00OO00O0000O000 =False #line:1209
                return OO00OO00O0000O000 #line:1210
            for O0OO0O00O00000000 in OO00O00000OO00OOO .get ('attributes'):#line:1211
                if (O0OO0O00O00000000 .get ('name'),None )==None :#line:1212
                    print (f"Error: cedent {OO0OOOOOO0O0OOO0O} / attribute {O0OO0O00O00000000} has no 'name' attribute specified.")#line:1213
                    OO00OO00O0000O000 =False #line:1214
                    return OO00OO00O0000O000 #line:1215
                if not ((O0OO0O00O00000000 .get ('name'))in self .data ["varname"]):#line:1216
                    print (f"Error: cedent {OO0OOOOOO0O0OOO0O} / attribute {O0OO0O00O00000000.get('name')} not in variable list. Please check spelling.")#line:1217
                    OO00OO00O0000O000 =False #line:1218
                    return OO00OO00O0000O000 #line:1219
                if (O0OO0O00O00000000 .get ('type'),None )==None :#line:1220
                    print (f"Error: cedent {OO0OOOOOO0O0OOO0O} / attribute {O0OO0O00O00000000.get('name')} has no 'type' attribute specified.")#line:1221
                    OO00OO00O0000O000 =False #line:1222
                    return OO00OO00O0000O000 #line:1223
                if not ((O0OO0O00O00000000 .get ('type'))in (['rcut','lcut','seq','subset','one','list'])):#line:1224
                    print (f"Error: cedent {OO0OOOOOO0O0OOO0O} / attribute {O0OO0O00O00000000.get('name')} has unsupported type {O0OO0O00O00000000.get('type')}. Supported types are 'subset','seq','lcut','rcut','one','list'.")#line:1225
                    OO00OO00O0000O000 =False #line:1226
                    return OO00OO00O0000O000 #line:1227
                if (O0OO0O00O00000000 .get ('minlen'),None )==None :#line:1228
                    print (f"Error: cedent {OO0OOOOOO0O0OOO0O} / attribute {O0OO0O00O00000000.get('name')} has no minimal length specified.")#line:1229
                    OO00OO00O0000O000 =False #line:1230
                    return OO00OO00O0000O000 #line:1231
                if not (type (O0OO0O00O00000000 .get ('minlen'))is int ):#line:1232
                    if not (O0OO0O00O00000000 .get ('type')=='one'or O0OO0O00O00000000 .get ('type')=='list'):#line:1233
                        print (f"Error: cedent {OO0OOOOOO0O0OOO0O} / attribute {O0OO0O00O00000000.get('name')} has invalid type of minimal length.")#line:1234
                        OO00OO00O0000O000 =False #line:1235
                        return OO00OO00O0000O000 #line:1236
                if (O0OO0O00O00000000 .get ('maxlen'),None )==None :#line:1237
                    print (f"Error: cedent {OO0OOOOOO0O0OOO0O} / attribute {O0OO0O00O00000000.get('name')} has no maximal length specified.")#line:1238
                    OO00OO00O0000O000 =False #line:1239
                    return OO00OO00O0000O000 #line:1240
                if not (type (O0OO0O00O00000000 .get ('maxlen'))is int ):#line:1241
                    if not (O0OO0O00O00000000 .get ('type')=='one'or O0OO0O00O00000000 .get ('type')=='list'):#line:1242
                        print (f"Error: cedent {OO0OOOOOO0O0OOO0O} / attribute {O0OO0O00O00000000.get('name')} has invalid type of maximal length.")#line:1243
                        OO00OO00O0000O000 =False #line:1244
                        return OO00OO00O0000O000 #line:1245
        return OO00OO00O0000O000 #line:1246
    def _calculate (self ,**O0000OOO00O0OO00O ):#line:1248
        if self .data ["data_prepared"]==0 :#line:1249
            print ("Error: data not prepared")#line:1250
            return #line:1251
        self .kwargs =O0000OOO00O0OO00O #line:1252
        self .proc =O0000OOO00O0OO00O .get ('proc')#line:1253
        self .quantifiers =O0000OOO00O0OO00O .get ('quantifiers')#line:1254
        self ._init_task ()#line:1256
        self .stats ['start_proc_time']=time .time ()#line:1257
        self .task_actinfo ['cedents_to_do']=[]#line:1258
        self .task_actinfo ['cedents']=[]#line:1259
        if O0000OOO00O0OO00O .get ("proc")=='UICMiner':#line:1262
            if not (self ._check_cedents (['ante'],**O0000OOO00O0OO00O )):#line:1263
                return #line:1264
            _OO00O000O0000O0O0 =O0000OOO00O0OO00O .get ("cond")#line:1266
            if _OO00O000O0000O0O0 !=None :#line:1267
                self .task_actinfo ['cedents_to_do'].append ('cond')#line:1268
            else :#line:1269
                O0OOOOO00000OO00O =self .cedent #line:1270
                O0OOOOO00000OO00O ['cedent_type']='cond'#line:1271
                O0OOOOO00000OO00O ['filter_value']=(1 <<self .data ["rows_count"])-1 #line:1272
                O0OOOOO00000OO00O ['generated_string']='---'#line:1273
                if self .verbosity ['debug']:#line:1274
                    print (O0OOOOO00000OO00O ['filter_value'])#line:1275
                self .task_actinfo ['cedents_to_do'].append ('cond')#line:1276
                self .task_actinfo ['cedents'].append (O0OOOOO00000OO00O )#line:1277
            self .task_actinfo ['cedents_to_do'].append ('ante')#line:1278
            if O0000OOO00O0OO00O .get ('target',None )==None :#line:1279
                print ("ERROR: no succedent/target variable defined for UIC Miner")#line:1280
                return #line:1281
            if not (O0000OOO00O0OO00O .get ('target')in self .data ["varname"]):#line:1282
                print ("ERROR: target parameter is not variable. Please check spelling of variable name in parameter 'target'.")#line:1283
                return #line:1284
            if ("aad_score"in self .quantifiers ):#line:1285
                if not ("aad_weights"in self .quantifiers ):#line:1286
                    print ("ERROR: for aad quantifier you need to specify aad weights.")#line:1287
                    return #line:1288
                if not (len (self .quantifiers .get ("aad_weights"))==len (self .data ["dm"][self .data ["varname"].index (self .kwargs .get ('target'))])):#line:1289
                    print ("ERROR: aad weights has different number of weights than classes of target variable.")#line:1290
                    return #line:1291
        elif O0000OOO00O0OO00O .get ("proc")=='CFMiner':#line:1292
            self .task_actinfo ['cedents_to_do']=['cond']#line:1293
            if O0000OOO00O0OO00O .get ('target',None )==None :#line:1294
                print ("ERROR: no target variable defined for CF Miner")#line:1295
                return #line:1296
            O0O00OO0O0OOO0000 =O0000OOO00O0OO00O .get ('target',None )#line:1297
            self .profiles ['hist_target_entire_dataset_labels']=self .data ["catnames"][self .data ["varname"].index (self .kwargs .get ('target'))]#line:1298
            OO00OOO0OOO0OOO00 =self .data ["dm"][self .data ["varname"].index (self .kwargs .get ('target'))]#line:1299
            O00OOOO0OOO0OOOOO =[]#line:1301
            for OOOOOO0000O00OOOO in range (len (OO00OOO0OOO0OOO00 )):#line:1302
                OOOOO0O0000OO0O00 =self ._bitcount (OO00OOO0OOO0OOO00 [OOOOOO0000O00OOOO ])#line:1303
                O00OOOO0OOO0OOOOO .append (OOOOO0O0000OO0O00 )#line:1304
            self .profiles ['hist_target_entire_dataset_values']=O00OOOO0OOO0OOOOO #line:1305
            if not (self ._check_cedents (['cond'],**O0000OOO00O0OO00O )):#line:1306
                return #line:1307
            if not (O0000OOO00O0OO00O .get ('target')in self .data ["varname"]):#line:1308
                print ("ERROR: target parameter is not variable. Please check spelling of variable name in parameter 'target'.")#line:1309
                return #line:1310
            if ("aad"in self .quantifiers ):#line:1311
                if not ("aad_weights"in self .quantifiers ):#line:1312
                    print ("ERROR: for aad quantifier you need to specify aad weights.")#line:1313
                    return #line:1314
                if not (len (self .quantifiers .get ("aad_weights"))==len (self .data ["dm"][self .data ["varname"].index (self .kwargs .get ('target'))])):#line:1315
                    print ("ERROR: aad weights has different number of weights than classes of target variable.")#line:1316
                    return #line:1317
        elif O0000OOO00O0OO00O .get ("proc")=='4ftMiner':#line:1320
            if not (self ._check_cedents (['ante','succ'],**O0000OOO00O0OO00O )):#line:1321
                return #line:1322
            _OO00O000O0000O0O0 =O0000OOO00O0OO00O .get ("cond")#line:1324
            if _OO00O000O0000O0O0 !=None :#line:1325
                self .task_actinfo ['cedents_to_do'].append ('cond')#line:1326
            else :#line:1327
                O0OOOOO00000OO00O =self .cedent #line:1328
                O0OOOOO00000OO00O ['cedent_type']='cond'#line:1329
                O0OOOOO00000OO00O ['filter_value']=(1 <<self .data ["rows_count"])-1 #line:1330
                O0OOOOO00000OO00O ['generated_string']='---'#line:1331
                self .task_actinfo ['cedents_to_do'].append ('cond')#line:1332
                self .task_actinfo ['cedents'].append (O0OOOOO00000OO00O )#line:1333
            self .task_actinfo ['cedents_to_do'].append ('ante')#line:1334
            self .task_actinfo ['cedents_to_do'].append ('succ')#line:1335
        elif O0000OOO00O0OO00O .get ("proc")=='SD4ftMiner':#line:1336
            if not (self ._check_cedents (['ante','succ','frst','scnd'],**O0000OOO00O0OO00O )):#line:1339
                return #line:1340
            _OO00O000O0000O0O0 =O0000OOO00O0OO00O .get ("cond")#line:1341
            if _OO00O000O0000O0O0 !=None :#line:1342
                self .task_actinfo ['cedents_to_do'].append ('cond')#line:1343
            else :#line:1344
                O0OOOOO00000OO00O =self .cedent #line:1345
                O0OOOOO00000OO00O ['cedent_type']='cond'#line:1346
                O0OOOOO00000OO00O ['filter_value']=(1 <<self .data ["rows_count"])-1 #line:1347
                O0OOOOO00000OO00O ['generated_string']='---'#line:1348
                self .task_actinfo ['cedents_to_do'].append ('cond')#line:1349
                self .task_actinfo ['cedents'].append (O0OOOOO00000OO00O )#line:1350
            self .task_actinfo ['cedents_to_do'].append ('frst')#line:1351
            self .task_actinfo ['cedents_to_do'].append ('scnd')#line:1352
            self .task_actinfo ['cedents_to_do'].append ('ante')#line:1353
            self .task_actinfo ['cedents_to_do'].append ('succ')#line:1354
        else :#line:1355
            print ("Unsupported procedure")#line:1356
            return #line:1357
        print ("Will go for ",O0000OOO00O0OO00O .get ("proc"))#line:1358
        self .task_actinfo ['optim']={}#line:1361
        OOOO0000OO0O0OO0O =True #line:1362
        for OOO00O0OO0000OO00 in self .task_actinfo ['cedents_to_do']:#line:1363
            try :#line:1364
                OO0O0OO00OOO0000O =self .kwargs .get (OOO00O0OO0000OO00 )#line:1365
                if self .verbosity ['debug']:#line:1366
                    print (OO0O0OO00OOO0000O )#line:1367
                    print (f"...cedent {OOO00O0OO0000OO00} is type {OO0O0OO00OOO0000O.get('type')}")#line:1368
                    print (f"Will check cedent type {OOO00O0OO0000OO00} : {OO0O0OO00OOO0000O.get('type')}")#line:1369
                if OO0O0OO00OOO0000O .get ('type')!='con':#line:1370
                    OOOO0000OO0O0OO0O =False #line:1371
                    if self .verbosity ['debug']:#line:1372
                        print (f"Cannot optim due to cedent type {OOO00O0OO0000OO00} : {OO0O0OO00OOO0000O.get('type')}")#line:1373
            except :#line:1374
                OOOOO0O00000O000O =1 <2 #line:1375
        if self .options ['optimizations']==False :#line:1377
            OOOO0000OO0O0OO0O =False #line:1378
        O00O00O0O0OOOO00O ={}#line:1379
        O00O00O0O0OOOO00O ['only_con']=OOOO0000OO0O0OO0O #line:1380
        self .task_actinfo ['optim']=O00O00O0O0OOOO00O #line:1381
        if self .verbosity ['debug']:#line:1385
            print ("Starting to prepare data.")#line:1386
            self ._prep_data (self .data .df )#line:1387
            self .stats ['mid1_time']=time .time ()#line:1388
            self .quantifiers =O0000OOO00O0OO00O .get ('self.quantifiers')#line:1389
        print ("Starting to mine rules.")#line:1390
        sys .stdout .flush ()#line:1391
        time .sleep (0.01 )#line:1392
        if self .options ['progressbar']:#line:1393
            O00OOO0OOO00OOO0O =[progressbar .Percentage (),progressbar .Bar (),progressbar .Timer ()]#line:1394
            self .bar =progressbar .ProgressBar (widgets =O00OOO0OOO00OOO0O ,max_value =100 ,fd =sys .stdout ).start ()#line:1395
            self .bar .update (0 )#line:1396
        self .progress_lower =0 #line:1397
        self .progress_upper =100 #line:1398
        self ._start_cedent (self .task_actinfo ,self .progress_lower ,self .progress_upper )#line:1399
        if self .options ['progressbar']:#line:1400
            self .bar .update (100 )#line:1401
            self .bar .finish ()#line:1402
        self .stats ['end_proc_time']=time .time ()#line:1403
        print ("Done. Total verifications : "+str (self .stats ['total_cnt'])+", rules "+str (self .stats ['total_valid'])+", times: prep "+"{:.2f}".format (self .stats ['end_prep_time']-self .stats ['start_prep_time'])+"sec, processing "+"{:.2f}".format (self .stats ['end_proc_time']-self .stats ['start_proc_time'])+"sec")#line:1406
        O0O00OO0O0O0OO0OO ={}#line:1407
        OOOO000OOO00OOOOO ={}#line:1408
        OOOO000OOO00OOOOO ["task_type"]=O0000OOO00O0OO00O .get ('proc')#line:1409
        OOOO000OOO00OOOOO ["target"]=O0000OOO00O0OO00O .get ('target')#line:1410
        OOOO000OOO00OOOOO ["self.quantifiers"]=self .quantifiers #line:1411
        if O0000OOO00O0OO00O .get ('cond')!=None :#line:1412
            OOOO000OOO00OOOOO ['cond']=O0000OOO00O0OO00O .get ('cond')#line:1413
        if O0000OOO00O0OO00O .get ('ante')!=None :#line:1414
            OOOO000OOO00OOOOO ['ante']=O0000OOO00O0OO00O .get ('ante')#line:1415
        if O0000OOO00O0OO00O .get ('succ')!=None :#line:1416
            OOOO000OOO00OOOOO ['succ']=O0000OOO00O0OO00O .get ('succ')#line:1417
        if O0000OOO00O0OO00O .get ('opts')!=None :#line:1418
            OOOO000OOO00OOOOO ['opts']=O0000OOO00O0OO00O .get ('opts')#line:1419
        if self .df is None :#line:1420
            OOOO000OOO00OOOOO ['rowcount']=self .data ["rows_count"]#line:1421
        else :#line:1423
            OOOO000OOO00OOOOO ['rowcount']=len (self .df .index )#line:1424
        O0O00OO0O0O0OO0OO ["taskinfo"]=OOOO000OOO00OOOOO #line:1425
        O0000OOOO00O0O00O ={}#line:1426
        O0000OOOO00O0O00O ["total_verifications"]=self .stats ['total_cnt']#line:1427
        O0000OOOO00O0O00O ["valid_rules"]=self .stats ['total_valid']#line:1428
        O0000OOOO00O0O00O ["total_verifications_with_opt"]=self .stats ['total_ver']#line:1429
        O0000OOOO00O0O00O ["time_prep"]=self .stats ['end_prep_time']-self .stats ['start_prep_time']#line:1430
        O0000OOOO00O0O00O ["time_processing"]=self .stats ['end_proc_time']-self .stats ['start_proc_time']#line:1431
        O0000OOOO00O0O00O ["time_total"]=self .stats ['end_prep_time']-self .stats ['start_prep_time']+self .stats ['end_proc_time']-self .stats ['start_proc_time']#line:1432
        O0O00OO0O0O0OO0OO ["summary_statistics"]=O0000OOOO00O0O00O #line:1433
        O0O00OO0O0O0OO0OO ["rules"]=self .rulelist #line:1434
        OOOOO0000OOO00OO0 ={}#line:1435
        OOOOO0000OOO00OO0 ["varname"]=self .data ["varname"]#line:1436
        OOOOO0000OOO00OO0 ["catnames"]=self .data ["catnames"]#line:1437
        O0O00OO0O0O0OO0OO ["datalabels"]=OOOOO0000OOO00OO0 #line:1438
        self .result =O0O00OO0O0O0OO0OO #line:1439
    def print_summary (self ):#line:1441
        """
        Prints the task processing summary.
        """#line:1444
        if not (self ._is_calculated ()):#line:1445
            print ("ERROR: Task has not been calculated.")#line:1446
            return #line:1447
        print ("")#line:1448
        print ("CleverMiner task processing summary:")#line:1449
        print ("")#line:1450
        print (f"Task type : {self.result['taskinfo']['task_type']}")#line:1451
        print (f"Number of verifications : {self.result['summary_statistics']['total_verifications']}")#line:1452
        print (f"Number of rules : {self.result['summary_statistics']['valid_rules']}")#line:1453
        print (f"Total time needed : {strftime('%Hh %Mm %Ss', gmtime(self.result['summary_statistics']['time_total']))}")#line:1454
        if self .verbosity ['debug']:#line:1455
            print (f"Total time needed : {self.result['summary_statistics']['time_total']}")#line:1456
        print (f"Time of data preparation : {strftime('%Hh %Mm %Ss', gmtime(self.result['summary_statistics']['time_prep']))}")#line:1457
        print (f"Time of rule mining : {strftime('%Hh %Mm %Ss', gmtime(self.result['summary_statistics']['time_processing']))}")#line:1458
        print ("")#line:1459
    def print_hypolist (self ):#line:1461
        """
        Prints the list of rules.
        """#line:1464
        self .print_rulelist ();#line:1465
    def print_rulelist (self ,sortby =None ,storesorted =False ):#line:1467
        """
        Prints the list of rules.
        :param str sortby: name of the quantifier by which output will be sorted
        :param bool storesorted: whether to keep sorted dataframe or not
        """#line:1472
        if not (self ._is_calculated ()):#line:1473
            print ("ERROR: Task has not been calculated.")#line:1474
            return #line:1475
        def O0O0OO0O0000O0O00 (item ):#line:1477
            OO00000OOOOO000OO =item ["params"]#line:1478
            return OO00000OOOOO000OO .get (sortby ,0 )#line:1479
        print ("")#line:1481
        print ("List of rules:")#line:1482
        if self .result ['taskinfo']['task_type']=="4ftMiner":#line:1483
            print ("RULEID BASE  CONF  AAD    Rule")#line:1484
        elif self .result ['taskinfo']['task_type']=="UICMiner":#line:1485
            print ("RULEID BASE  AAD_SCORE  Rule")#line:1486
        elif self .result ['taskinfo']['task_type']=="CFMiner":#line:1487
            print ("RULEID BASE  S_UP  S_DOWN Condition")#line:1488
        elif self .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1489
            print ("RULEID BASE1 BASE2 RatioConf DeltaConf Rule")#line:1490
        else :#line:1491
            print ("Unsupported task type for rulelist")#line:1492
            return #line:1493
        OOO000000000O00O0 =self .result ["rules"]#line:1494
        if sortby is not None :#line:1495
            OOO000000000O00O0 =sorted (OOO000000000O00O0 ,key =O0O0OO0O0000O0O00 ,reverse =True )#line:1496
            if storesorted :#line:1497
                self .result ["rules"]=OOO000000000O00O0 #line:1498
        for OOOO00000O00OOO00 in OOO000000000O00O0 :#line:1500
            OOO0OOO0O0OOO00O0 ="{:6d}".format (OOOO00000O00OOO00 ["rule_id"])#line:1501
            if self .result ['taskinfo']['task_type']=="4ftMiner":#line:1502
                if self .verbosity ['debug']:#line:1503
                   print (f"{OOOO00000O00OOO00['params']}")#line:1504
                OOO0OOO0O0OOO00O0 =OOO0OOO0O0OOO00O0 +" "+"{:5d}".format (OOOO00000O00OOO00 ["params"]["base"])+" "+"{:.3f}".format (OOOO00000O00OOO00 ["params"]["conf"])+" "+"{:+.3f}".format (OOOO00000O00OOO00 ["params"]["aad"])#line:1505
                OOO0OOO0O0OOO00O0 =OOO0OOO0O0OOO00O0 +" "+OOOO00000O00OOO00 ["cedents_str"]["ante"]+" => "+OOOO00000O00OOO00 ["cedents_str"]["succ"]+" | "+OOOO00000O00OOO00 ["cedents_str"]["cond"]#line:1506
            elif self .result ['taskinfo']['task_type']=="UICMiner":#line:1507
                OOO0OOO0O0OOO00O0 =OOO0OOO0O0OOO00O0 +" "+"{:5d}".format (OOOO00000O00OOO00 ["params"]["base"])+" "+"{:.3f}".format (OOOO00000O00OOO00 ["params"]["aad_score"])#line:1508
                OOO0OOO0O0OOO00O0 =OOO0OOO0O0OOO00O0 +"     "+OOOO00000O00OOO00 ["cedents_str"]["ante"]+" => "+self .result ['taskinfo']['target']+"(*) | "+OOOO00000O00OOO00 ["cedents_str"]["cond"]#line:1509
            elif self .result ['taskinfo']['task_type']=="CFMiner":#line:1510
                OOO0OOO0O0OOO00O0 =OOO0OOO0O0OOO00O0 +" "+"{:5d}".format (OOOO00000O00OOO00 ["params"]["base"])+" "+"{:5d}".format (OOOO00000O00OOO00 ["params"]["s_up"])+" "+"{:5d}".format (OOOO00000O00OOO00 ["params"]["s_down"])#line:1511
                OOO0OOO0O0OOO00O0 =OOO0OOO0O0OOO00O0 +" "+OOOO00000O00OOO00 ["cedents_str"]["cond"]#line:1512
            elif self .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1513
                OOO0OOO0O0OOO00O0 =OOO0OOO0O0OOO00O0 +" "+"{:5d}".format (OOOO00000O00OOO00 ["params"]["base1"])+" "+"{:5d}".format (OOOO00000O00OOO00 ["params"]["base2"])+"    "+"{:.3f}".format (OOOO00000O00OOO00 ["params"]["ratioconf"])+"    "+"{:+.3f}".format (OOOO00000O00OOO00 ["params"]["deltaconf"])#line:1514
                OOO0OOO0O0OOO00O0 =OOO0OOO0O0OOO00O0 +"  "+OOOO00000O00OOO00 ["cedents_str"]["ante"]+" => "+OOOO00000O00OOO00 ["cedents_str"]["succ"]+" | "+OOOO00000O00OOO00 ["cedents_str"]["cond"]+" : "+OOOO00000O00OOO00 ["cedents_str"]["frst"]+" x "+OOOO00000O00OOO00 ["cedents_str"]["scnd"]#line:1515
            print (OOO0OOO0O0OOO00O0 )#line:1517
        print ("")#line:1518
    def print_hypo (self ,rule_id ):#line:1520
        """
        Prints the specified rule to the text output
        :param rule_id: identification of the rule (rule number) to be printed
        """#line:1524
        self .print_rule (rule_id )#line:1525
    def print_rule (self ,rule_id ):#line:1528
        """
        Prints the specified rule to the text output
        :param rule_id: identification of the rule (rule number) to be printed
        """#line:1532
        if not (self ._is_calculated ()):#line:1533
            print ("ERROR: Task has not been calculated.")#line:1534
            return #line:1535
        print ("")#line:1536
        if (rule_id <=len (self .result ["rules"])):#line:1537
            if self .result ['taskinfo']['task_type']=="4ftMiner":#line:1538
                print ("")#line:1539
                O000O000O00OOO0O0 =self .result ["rules"][rule_id -1 ]#line:1540
                print (f"Rule id : {O000O000O00OOO0O0['rule_id']}")#line:1541
                print ("")#line:1542
                print (f"Base : {'{:5d}'.format(O000O000O00OOO0O0['params']['base'])}  Relative base : {'{:.3f}'.format(O000O000O00OOO0O0['params']['rel_base'])}  CONF : {'{:.3f}'.format(O000O000O00OOO0O0['params']['conf'])}  AAD : {'{:+.3f}'.format(O000O000O00OOO0O0['params']['aad'])}  BAD : {'{:+.3f}'.format(O000O000O00OOO0O0['params']['bad'])}")#line:1543
                print ("")#line:1544
                print ("Cedents:")#line:1545
                print (f"  antecedent : {O000O000O00OOO0O0['cedents_str']['ante']}")#line:1546
                print (f"  succcedent : {O000O000O00OOO0O0['cedents_str']['succ']}")#line:1547
                print (f"  condition  : {O000O000O00OOO0O0['cedents_str']['cond']}")#line:1548
                print ("")#line:1549
                print ("Fourfold table")#line:1550
                print (f"    |  S  |  ¬S |")#line:1551
                print (f"----|-----|-----|")#line:1552
                print (f" A  |{'{:5d}'.format(O000O000O00OOO0O0['params']['fourfold'][0])}|{'{:5d}'.format(O000O000O00OOO0O0['params']['fourfold'][1])}|")#line:1553
                print (f"----|-----|-----|")#line:1554
                print (f"¬A  |{'{:5d}'.format(O000O000O00OOO0O0['params']['fourfold'][2])}|{'{:5d}'.format(O000O000O00OOO0O0['params']['fourfold'][3])}|")#line:1555
                print (f"----|-----|-----|")#line:1556
            elif self .result ['taskinfo']['task_type']=="CFMiner":#line:1557
                print ("")#line:1558
                O000O000O00OOO0O0 =self .result ["rules"][rule_id -1 ]#line:1559
                print (f"Rule id : {O000O000O00OOO0O0['rule_id']}")#line:1560
                print ("")#line:1561
                O0OOOOOOOO0000O00 =""#line:1562
                if ('aad'in O000O000O00OOO0O0 ['params']):#line:1563
                    O0OOOOOOOO0000O00 ="aad : "+str (O000O000O00OOO0O0 ['params']['aad'])#line:1564
                print (f"Base : {'{:5d}'.format(O000O000O00OOO0O0['params']['base'])}  Relative base : {'{:.3f}'.format(O000O000O00OOO0O0['params']['rel_base'])}  Steps UP (consecutive) : {'{:5d}'.format(O000O000O00OOO0O0['params']['s_up'])}  Steps DOWN (consecutive) : {'{:5d}'.format(O000O000O00OOO0O0['params']['s_down'])}  Steps UP (any) : {'{:5d}'.format(O000O000O00OOO0O0['params']['s_any_up'])}  Steps DOWN (any) : {'{:5d}'.format(O000O000O00OOO0O0['params']['s_any_down'])}  Histogram maximum : {'{:5d}'.format(O000O000O00OOO0O0['params']['max'])}  Histogram minimum : {'{:5d}'.format(O000O000O00OOO0O0['params']['min'])}  Histogram relative maximum : {'{:.3f}'.format(O000O000O00OOO0O0['params']['rel_max'])} Histogram relative minimum : {'{:.3f}'.format(O000O000O00OOO0O0['params']['rel_min'])} {O0OOOOOOOO0000O00}")#line:1566
                print ("")#line:1567
                print (f"Condition  : {O000O000O00OOO0O0['cedents_str']['cond']}")#line:1568
                print ("")#line:1569
                O00OOO0O0OO00OOOO =self .get_category_names (self .result ["taskinfo"]["target"])#line:1570
                print (f"Categories in target variable  {O00OOO0O0OO00OOOO}")#line:1571
                print (f"Histogram                      {O000O000O00OOO0O0['params']['hist']}")#line:1572
                if ('aad'in O000O000O00OOO0O0 ['params']):#line:1573
                    print (f"Histogram on full set          {O000O000O00OOO0O0['params']['hist_full']}")#line:1574
                    print (f"Relative histogram             {O000O000O00OOO0O0['params']['rel_hist']}")#line:1575
                    print (f"Relative histogram on full set {O000O000O00OOO0O0['params']['rel_hist_full']}")#line:1576
            elif self .result ['taskinfo']['task_type']=="UICMiner":#line:1577
                print ("")#line:1578
                O000O000O00OOO0O0 =self .result ["rules"][rule_id -1 ]#line:1579
                print (f"Rule id : {O000O000O00OOO0O0['rule_id']}")#line:1580
                print ("")#line:1581
                O0OOOOOOOO0000O00 =""#line:1582
                if ('aad_score'in O000O000O00OOO0O0 ['params']):#line:1583
                    O0OOOOOOOO0000O00 ="aad score : "+str (O000O000O00OOO0O0 ['params']['aad_score'])#line:1584
                print (f"Base : {'{:5d}'.format(O000O000O00OOO0O0['params']['base'])}  Relative base : {'{:.3f}'.format(O000O000O00OOO0O0['params']['rel_base'])}   {O0OOOOOOOO0000O00}")#line:1586
                print ("")#line:1587
                print (f"Condition  : {O000O000O00OOO0O0['cedents_str']['cond']}")#line:1588
                print (f"Antecedent : {O000O000O00OOO0O0['cedents_str']['ante']}")#line:1589
                print ("")#line:1590
                print (f"Histogram                                        {O000O000O00OOO0O0['params']['hist']}")#line:1591
                if ('aad_score'in O000O000O00OOO0O0 ['params']):#line:1592
                    print (f"Histogram on full set with condition             {O000O000O00OOO0O0['params']['hist_cond']}")#line:1593
                    print (f"Relative histogram                               {O000O000O00OOO0O0['params']['rel_hist']}")#line:1594
                    print (f"Relative histogram on full set with condition    {O000O000O00OOO0O0['params']['rel_hist_cond']}")#line:1595
                OOOOOOO0O000O000O =self .result ['datalabels']['catnames'][self .result ['datalabels']['varname'].index (self .result ['taskinfo']['target'])]#line:1596
                print (" ")#line:1597
                print ("Interpretation:")#line:1598
                for OO0O00000O00OO0OO in range (len (OOOOOOO0O000O000O )):#line:1599
                  O0O0000OOO0O00OO0 =0 #line:1600
                  if O000O000O00OOO0O0 ['params']['rel_hist'][OO0O00000O00OO0OO ]>0 :#line:1601
                      O0O0000OOO0O00OO0 =O000O000O00OOO0O0 ['params']['rel_hist'][OO0O00000O00OO0OO ]/O000O000O00OOO0O0 ['params']['rel_hist_cond'][OO0O00000O00OO0OO ]#line:1602
                  O0O00OO0O000O0O0O =''#line:1603
                  if not (O000O000O00OOO0O0 ['cedents_str']['cond']=='---'):#line:1604
                      O0O00OO0O000O0O0O ="For "+O000O000O00OOO0O0 ['cedents_str']['cond']+": "#line:1605
                  print (f"    {O0O00OO0O000O0O0O}{self.result['taskinfo']['target']}({OOOOOOO0O000O000O[OO0O00000O00OO0OO]}) has occurence {'{:.1%}'.format(O000O000O00OOO0O0['params']['rel_hist_cond'][OO0O00000O00OO0OO])}, with antecedent it has occurence {'{:.1%}'.format(O000O000O00OOO0O0['params']['rel_hist'][OO0O00000O00OO0OO])}, that is {'{:.3f}'.format(O0O0000OOO0O00OO0)} times more.")#line:1607
            elif self .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1608
                print ("")#line:1609
                O000O000O00OOO0O0 =self .result ["rules"][rule_id -1 ]#line:1610
                print (f"Rule id : {O000O000O00OOO0O0['rule_id']}")#line:1611
                print ("")#line:1612
                print (f"Base1 : {'{:5d}'.format(O000O000O00OOO0O0['params']['base1'])} Base2 : {'{:5d}'.format(O000O000O00OOO0O0['params']['base2'])}  Relative base 1 : {'{:.3f}'.format(O000O000O00OOO0O0['params']['rel_base1'])} Relative base 2 : {'{:.3f}'.format(O000O000O00OOO0O0['params']['rel_base2'])} CONF1 : {'{:.3f}'.format(O000O000O00OOO0O0['params']['conf1'])}  CONF2 : {'{:+.3f}'.format(O000O000O00OOO0O0['params']['conf2'])}  Delta Conf : {'{:+.3f}'.format(O000O000O00OOO0O0['params']['deltaconf'])} Ratio Conf : {'{:+.3f}'.format(O000O000O00OOO0O0['params']['ratioconf'])}")#line:1613
                print ("")#line:1614
                print ("Cedents:")#line:1615
                print (f"  antecedent : {O000O000O00OOO0O0['cedents_str']['ante']}")#line:1616
                print (f"  succcedent : {O000O000O00OOO0O0['cedents_str']['succ']}")#line:1617
                print (f"  condition  : {O000O000O00OOO0O0['cedents_str']['cond']}")#line:1618
                print (f"  first set  : {O000O000O00OOO0O0['cedents_str']['frst']}")#line:1619
                print (f"  second set : {O000O000O00OOO0O0['cedents_str']['scnd']}")#line:1620
                print ("")#line:1621
                print ("Fourfold tables:")#line:1622
                print (f"FRST|  S  |  ¬S |  SCND|  S  |  ¬S |");#line:1623
                print (f"----|-----|-----|  ----|-----|-----| ")#line:1624
                print (f" A  |{'{:5d}'.format(O000O000O00OOO0O0['params']['fourfold1'][0])}|{'{:5d}'.format(O000O000O00OOO0O0['params']['fourfold1'][1])}|   A  |{'{:5d}'.format(O000O000O00OOO0O0['params']['fourfold2'][0])}|{'{:5d}'.format(O000O000O00OOO0O0['params']['fourfold2'][1])}|")#line:1625
                print (f"----|-----|-----|  ----|-----|-----|")#line:1626
                print (f"¬A  |{'{:5d}'.format(O000O000O00OOO0O0['params']['fourfold1'][2])}|{'{:5d}'.format(O000O000O00OOO0O0['params']['fourfold1'][3])}|  ¬A  |{'{:5d}'.format(O000O000O00OOO0O0['params']['fourfold2'][2])}|{'{:5d}'.format(O000O000O00OOO0O0['params']['fourfold2'][3])}|")#line:1627
                print (f"----|-----|-----|  ----|-----|-----|")#line:1628
            else :#line:1629
                print ("Unsupported task type for rule details")#line:1630
            print ("")#line:1634
        else :#line:1635
            print ("No such rule.")#line:1636
    def get_ruletext (self ,rule_id ):#line:1638
        """
        Gets text for the rule. Can be used in further processing.
        :param int rule_id: identification of the rule (rule number)
        :return: text for the specified rule
        :rtype: str
        """#line:1644
        if not (self ._is_calculated ()):#line:1645
            print ("ERROR: Task has not been calculated.")#line:1646
            return #line:1647
        if rule_id <=0 or rule_id >self .get_rulecount ():#line:1648
            if self .get_rulecount ()==0 :#line:1649
                print ("No such rule. There are no rules in result.")#line:1650
            else :#line:1651
                print (f"No such rule ({rule_id}). Available rules are 1 to {self.get_rulecount()}")#line:1652
            return None #line:1653
        OOO00OO00O0OO00O0 =""#line:1654
        OO0OO00O0O0OO0OO0 =self .result ["rules"][rule_id -1 ]#line:1655
        if self .result ['taskinfo']['task_type']=="4ftMiner":#line:1656
            OOO00OO00O0OO00O0 =OOO00OO00O0OO00O0 +" "+OO0OO00O0O0OO0OO0 ["cedents_str"]["ante"]+" => "+OO0OO00O0O0OO0OO0 ["cedents_str"]["succ"]+" | "+OO0OO00O0O0OO0OO0 ["cedents_str"]["cond"]#line:1658
        elif self .result ['taskinfo']['task_type']=="UICMiner":#line:1659
            OOO00OO00O0OO00O0 =OOO00OO00O0OO00O0 +"     "+OO0OO00O0O0OO0OO0 ["cedents_str"]["ante"]+" => "+self .result ['taskinfo']['target']+"(*) | "+OO0OO00O0O0OO0OO0 ["cedents_str"]["cond"]#line:1661
        elif self .result ['taskinfo']['task_type']=="CFMiner":#line:1662
            OOO00OO00O0OO00O0 =OOO00OO00O0OO00O0 +" "+OO0OO00O0O0OO0OO0 ["cedents_str"]["cond"]#line:1663
        elif self .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1664
            OOO00OO00O0OO00O0 =OOO00OO00O0OO00O0 +"  "+OO0OO00O0O0OO0OO0 ["cedents_str"]["ante"]+" => "+OO0OO00O0O0OO0OO0 ["cedents_str"]["succ"]+" | "+OO0OO00O0O0OO0OO0 ["cedents_str"]["cond"]+" : "+OO0OO00O0O0OO0OO0 ["cedents_str"]["frst"]+" x "+OO0OO00O0O0OO0OO0 ["cedents_str"]["scnd"]#line:1666
        return OOO00OO00O0OO00O0 #line:1667
    def _annotate_chart (self ,ax ,total ,cnt =2 ):#line:1669
        """
        Internal subroutine for graph annotation.
        :param ax: graph to annotate
        :param total: sum of all counts behind the bars in the chart
        :param cnt: how many bars are displayed in chart
        :return:
        """#line:1676
        OOOOOO00OO000OOOO =ax .axes .get_ylim ()#line:1677
        for O0O0OO0OO0OO00000 in ax .patches :#line:1679
            OO00O000O0O0OO00O ='{:.1f}%'.format (100 *O0O0OO0OO0OO00000 .get_height ()/total )#line:1680
            O0OOO000OO0OO0O00 =O0O0OO0OO0OO00000 .get_x ()+O0O0OO0OO0OO00000 .get_width ()/4 #line:1681
            OOOO0OOOO0O00O00O =O0O0OO0OO0OO00000 .get_y ()+O0O0OO0OO0OO00000 .get_height ()-OOOOOO00OO000OOOO [1 ]/8 #line:1682
            if O0O0OO0OO0OO00000 .get_height ()<OOOOOO00OO000OOOO [1 ]/8 :#line:1683
                OOOO0OOOO0O00O00O =O0O0OO0OO0OO00000 .get_y ()+O0O0OO0OO0OO00000 .get_height ()+OOOOOO00OO000OOOO [1 ]*0.02 #line:1684
            ax .annotate (OO00O000O0O0OO00O ,(O0OOO000OO0OO0O00 ,OOOO0OOOO0O00O00O ),size =23 /cnt )#line:1685
    def draw_rule (self ,rule_id ,show =True ,filename =None ):#line:1687
        """
        Show illustration chart for the specified rule.
        :param int rule_id: identification of the rule (rule number) to be shown
        :param bool show: whether to show chart to graphical output or not
        :param str filename: if specified, chart will be saved into this filename
        """#line:1693
        if not (self ._is_calculated ()):#line:1694
            print ("ERROR: Task has not been calculated.")#line:1695
            return #line:1696
        print ("")#line:1697
        if (rule_id <=len (self .result ["rules"])):#line:1698
            if self .result ['taskinfo']['task_type']=="4ftMiner":#line:1699
                O000O0OOOO0OO00OO ,O00000O0O0O0O0OO0 =plt .subplots (2 ,2 )#line:1701
                OOO0OO000OO0OOOOO =['S','not S']#line:1702
                OO0O0O0O000O000OO =['A','not A']#line:1703
                OOO000OOOOOOOOO00 =self .get_fourfold (rule_id )#line:1704
                O000OO0O000OO00O0 =[OOO000OOOOOOOOO00 [0 ],OOO000OOOOOOOOO00 [1 ]]#line:1706
                OOO0O0O0O0O0OOO00 =[OOO000OOOOOOOOO00 [2 ],OOO000OOOOOOOOO00 [3 ]]#line:1707
                OO000O0OO0OO00000 =[OOO000OOOOOOOOO00 [0 ]+OOO000OOOOOOOOO00 [2 ],OOO000OOOOOOOOO00 [1 ]+OOO000OOOOOOOOO00 [3 ]]#line:1708
                O00000O0O0O0O0OO0 [0 ,0 ]=sns .barplot (ax =O00000O0O0O0O0OO0 [0 ,0 ],x =OOO0OO000OO0OOOOO ,y =O000OO0O000OO00O0 ,color ='lightsteelblue')#line:1709
                self ._annotate_chart (O00000O0O0O0O0OO0 [0 ,0 ],OOO000OOOOOOOOO00 [0 ]+OOO000OOOOOOOOO00 [1 ])#line:1711
                O00000O0O0O0O0OO0 [0 ,1 ]=sns .barplot (ax =O00000O0O0O0O0OO0 [0 ,1 ],x =OOO0OO000OO0OOOOO ,y =OO000O0OO0OO00000 ,color ="gray",edgecolor ="black")#line:1713
                self ._annotate_chart (O00000O0O0O0O0OO0 [0 ,1 ],sum (OOO000OOOOOOOOO00 ))#line:1715
                O00000O0O0O0O0OO0 [0 ,0 ].set (xlabel =None ,ylabel ='Count')#line:1717
                O00000O0O0O0O0OO0 [0 ,1 ].set (xlabel =None ,ylabel ='Count')#line:1718
                OOOO0OO000O00OOO0 =sns .color_palette ("Blues",as_cmap =True )#line:1720
                O0O0OO0OO00OO0OOO =sns .color_palette ("Greys",as_cmap =True )#line:1721
                O00000O0O0O0O0OO0 [1 ,0 ]=sns .heatmap (ax =O00000O0O0O0O0OO0 [1 ,0 ],data =[O000OO0O000OO00O0 ,OOO0O0O0O0O0OOO00 ],xticklabels =OOO0OO000OO0OOOOO ,yticklabels =OO0O0O0O000O000OO ,annot =True ,cbar =False ,fmt =".0f",cmap =OOOO0OO000O00OOO0 )#line:1725
                O00000O0O0O0O0OO0 [1 ,0 ].set (xlabel =None ,ylabel ='Count')#line:1727
                O00000O0O0O0O0OO0 [1 ,1 ]=sns .heatmap (ax =O00000O0O0O0O0OO0 [1 ,1 ],data =np .asarray ([OO000O0OO0OO00000 ]),xticklabels =OOO0OO000OO0OOOOO ,yticklabels =False ,annot =True ,cbar =False ,fmt =".0f",cmap =O0O0OO0OO00OO0OOO )#line:1731
                O00000O0O0O0O0OO0 [1 ,1 ].set (xlabel =None ,ylabel ='Count')#line:1733
                OOOOOO0OO000O00OO =self .result ["rules"][rule_id -1 ]['cedents_str']['ante']#line:1735
                O00000O0O0O0O0OO0 [0 ,0 ].set (title ="\n".join (wrap (OOOOOO0OO000O00OO ,30 )))#line:1736
                O00000O0O0O0O0OO0 [0 ,1 ].set (title ='Entire dataset')#line:1737
                O0O0O0000OOO00OOO =self .result ["rules"][rule_id -1 ]['cedents_str']#line:1739
                O000O0OOOO0OO00OO .suptitle ("Antecedent : "+O0O0O0000OOO00OOO ['ante']+"\nSuccedent : "+O0O0O0000OOO00OOO ['succ']+"\nCondition : "+O0O0O0000OOO00OOO ['cond'],x =0 ,ha ='left',size ='small')#line:1743
                O000O0OOOO0OO00OO .tight_layout ()#line:1744
            elif self .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1746
                O000O0OOOO0OO00OO ,O00000O0O0O0O0OO0 =plt .subplots (2 ,2 )#line:1748
                OOO0OO000OO0OOOOO =['S','not S']#line:1749
                OO0O0O0O000O000OO =['A','not A']#line:1750
                O000OO0OOO0OO0000 =self .get_fourfold (rule_id ,order =1 )#line:1752
                OO0OOO0O0O0O0O0O0 =self .get_fourfold (rule_id ,order =2 )#line:1753
                OO0O00OOO0OO00O0O =[O000OO0OOO0OO0000 [0 ],O000OO0OOO0OO0000 [1 ]]#line:1755
                OO0O0O00O0000OO00 =[O000OO0OOO0OO0000 [2 ],O000OO0OOO0OO0000 [3 ]]#line:1756
                OOO0000000O0O0OO0 =[O000OO0OOO0OO0000 [0 ]+O000OO0OOO0OO0000 [2 ],O000OO0OOO0OO0000 [1 ]+O000OO0OOO0OO0000 [3 ]]#line:1757
                OOO0O00O0000OOO0O =[OO0OOO0O0O0O0O0O0 [0 ],OO0OOO0O0O0O0O0O0 [1 ]]#line:1758
                OOOOOO00O00O0OOO0 =[OO0OOO0O0O0O0O0O0 [2 ],OO0OOO0O0O0O0O0O0 [3 ]]#line:1759
                O0000OOOOO000OOO0 =[OO0OOO0O0O0O0O0O0 [0 ]+OO0OOO0O0O0O0O0O0 [2 ],OO0OOO0O0O0O0O0O0 [1 ]+OO0OOO0O0O0O0O0O0 [3 ]]#line:1760
                O00000O0O0O0O0OO0 [0 ,0 ]=sns .barplot (ax =O00000O0O0O0O0OO0 [0 ,0 ],x =OOO0OO000OO0OOOOO ,y =OO0O00OOO0OO00O0O ,color ='orange')#line:1761
                self ._annotate_chart (O00000O0O0O0O0OO0 [0 ,0 ],O000OO0OOO0OO0000 [0 ]+O000OO0OOO0OO0000 [1 ])#line:1763
                O00000O0O0O0O0OO0 [0 ,1 ]=sns .barplot (ax =O00000O0O0O0O0OO0 [0 ,1 ],x =OOO0OO000OO0OOOOO ,y =OOO0O00O0000OOO0O ,color ="green")#line:1765
                self ._annotate_chart (O00000O0O0O0O0OO0 [0 ,1 ],OO0OOO0O0O0O0O0O0 [0 ]+OO0OOO0O0O0O0O0O0 [1 ])#line:1767
                O00000O0O0O0O0OO0 [0 ,0 ].set (xlabel =None ,ylabel ='Count')#line:1769
                O00000O0O0O0O0OO0 [0 ,1 ].set (xlabel =None ,ylabel ='Count')#line:1770
                OOOO0OO000O00OOO0 =sns .color_palette ("Oranges",as_cmap =True )#line:1772
                O0O0OO0OO00OO0OOO =sns .color_palette ("Greens",as_cmap =True )#line:1773
                O00000O0O0O0O0OO0 [1 ,0 ]=sns .heatmap (ax =O00000O0O0O0O0OO0 [1 ,0 ],data =[OO0O00OOO0OO00O0O ,OO0O0O00O0000OO00 ],xticklabels =OOO0OO000OO0OOOOO ,yticklabels =OO0O0O0O000O000OO ,annot =True ,cbar =False ,fmt =".0f",cmap =OOOO0OO000O00OOO0 )#line:1776
                O00000O0O0O0O0OO0 [1 ,0 ].set (xlabel =None ,ylabel ='Count')#line:1778
                O00000O0O0O0O0OO0 [1 ,1 ]=sns .heatmap (ax =O00000O0O0O0O0OO0 [1 ,1 ],data =[OOO0O00O0000OOO0O ,OOOOOO00O00O0OOO0 ],xticklabels =OOO0OO000OO0OOOOO ,yticklabels =False ,annot =True ,cbar =False ,fmt =".0f",cmap =O0O0OO0OO00OO0OOO )#line:1782
                O00000O0O0O0O0OO0 [1 ,1 ].set (xlabel =None ,ylabel ='Count')#line:1784
                OOOOOO0OO000O00OO =self .result ["rules"][rule_id -1 ]['cedents_str']['frst']#line:1786
                O00000O0O0O0O0OO0 [0 ,0 ].set (title ="\n".join (wrap (OOOOOO0OO000O00OO ,30 )))#line:1787
                O0000O0000OOOOOOO =self .result ["rules"][rule_id -1 ]['cedents_str']['scnd']#line:1788
                O00000O0O0O0O0OO0 [0 ,1 ].set (title ="\n".join (wrap (O0000O0000OOOOOOO ,30 )))#line:1789
                O0O0O0000OOO00OOO =self .result ["rules"][rule_id -1 ]['cedents_str']#line:1791
                O000O0OOOO0OO00OO .suptitle ("Antecedent : "+O0O0O0000OOO00OOO ['ante']+"\nSuccedent : "+O0O0O0000OOO00OOO ['succ']+"\nCondition : "+O0O0O0000OOO00OOO ['cond']+"\nFirst : "+O0O0O0000OOO00OOO ['frst']+"\nSecond : "+O0O0O0000OOO00OOO ['scnd'],x =0 ,ha ='left',size ='small')#line:1796
                O000O0OOOO0OO00OO .tight_layout ()#line:1798
            elif (self .result ['taskinfo']['task_type']=="CFMiner")or (self .result ['taskinfo']['task_type']=="UICMiner"):#line:1801
                O0000OOOOO0O0OO0O =self .result ['taskinfo']['task_type']=="UICMiner"#line:1802
                O000O0OOOO0OO00OO ,O00000O0O0O0O0OO0 =plt .subplots (2 ,2 ,gridspec_kw ={'height_ratios':[3 ,1 ]})#line:1803
                OO0OO0O000O0OO0OO =self .result ['taskinfo']['target']#line:1804
                OOO0OO000OO0OOOOO =self .result ['datalabels']['catnames'][self .result ['datalabels']['varname'].index (self .result ['taskinfo']['target'])]#line:1806
                O0OOO000OO00O0000 =self .result ["rules"][rule_id -1 ]#line:1807
                O0O00OO0O0OO0000O =self .get_hist (rule_id )#line:1808
                if O0000OOOOO0O0OO0O :#line:1809
                    O0O00OO0O0OO0000O =O0OOO000OO00O0000 ['params']['hist']#line:1810
                else :#line:1811
                    O0O00OO0O0OO0000O =self .get_hist (rule_id )#line:1812
                O00000O0O0O0O0OO0 [0 ,0 ]=sns .barplot (ax =O00000O0O0O0O0OO0 [0 ,0 ],x =OOO0OO000OO0OOOOO ,y =O0O00OO0O0OO0000O ,color ='lightsteelblue')#line:1813
                OO0OOOO00OOOOO00O =[]#line:1815
                O0OO00O000O0O000O =[]#line:1816
                if O0000OOOOO0O0OO0O :#line:1817
                    OO0OOOO00OOOOO00O =OOO0OO000OO0OOOOO #line:1818
                    O0OO00O000O0O000O =self .get_hist (rule_id ,fullCond =True )#line:1819
                else :#line:1820
                    OO0OOOO00OOOOO00O =self .profiles ['hist_target_entire_dataset_labels']#line:1821
                    O0OO00O000O0O000O =self .profiles ['hist_target_entire_dataset_values']#line:1822
                O00000O0O0O0O0OO0 [0 ,1 ]=sns .barplot (ax =O00000O0O0O0O0OO0 [0 ,1 ],x =OO0OOOO00OOOOO00O ,y =O0OO00O000O0O000O ,color ="gray",edgecolor ="black")#line:1823
                self ._annotate_chart (O00000O0O0O0O0OO0 [0 ,0 ],sum (O0O00OO0O0OO0000O ),len (O0O00OO0O0OO0000O ))#line:1825
                self ._annotate_chart (O00000O0O0O0O0OO0 [0 ,1 ],sum (O0OO00O000O0O000O ),len (O0OO00O000O0O000O ))#line:1826
                O00000O0O0O0O0OO0 [0 ,0 ].set (xlabel =None ,ylabel ='Count')#line:1828
                O00000O0O0O0O0OO0 [0 ,1 ].set (xlabel =None ,ylabel ='Count')#line:1829
                OO000O00O000OOO00 =[OOO0OO000OO0OOOOO ,O0O00OO0O0OO0000O ]#line:1831
                OO0O0OOO0OOOOOOOO =pd .DataFrame (OO000O00O000OOO00 ).transpose ()#line:1832
                OO0O0OOO0OOOOOOOO .columns =[OO0OO0O000O0OO0OO ,'No of observatios']#line:1833
                OOOO0OO000O00OOO0 =sns .color_palette ("Blues",as_cmap =True )#line:1835
                O0O0OO0OO00OO0OOO =sns .color_palette ("Greys",as_cmap =True )#line:1836
                O00000O0O0O0O0OO0 [1 ,0 ]=sns .heatmap (ax =O00000O0O0O0O0OO0 [1 ,0 ],data =np .asarray ([O0O00OO0O0OO0000O ]),xticklabels =OOO0OO000OO0OOOOO ,yticklabels =False ,annot =True ,cbar =False ,fmt =".0f",cmap =OOOO0OO000O00OOO0 )#line:1840
                O00000O0O0O0O0OO0 [1 ,0 ].set (xlabel =OO0OO0O000O0OO0OO ,ylabel ='Count')#line:1842
                O00000O0O0O0O0OO0 [1 ,1 ]=sns .heatmap (ax =O00000O0O0O0O0OO0 [1 ,1 ],data =np .asarray ([O0OO00O000O0O000O ]),xticklabels =OO0OOOO00OOOOO00O ,yticklabels =False ,annot =True ,cbar =False ,fmt =".0f",cmap =O0O0OO0OO00OO0OOO )#line:1846
                O00000O0O0O0O0OO0 [1 ,1 ].set (xlabel =OO0OO0O000O0OO0OO ,ylabel ='Count')#line:1848
                OOO0O000OOOO00O0O =""#line:1849
                OO0O0OO0O0000O000 ='Entire dataset'#line:1850
                if O0000OOOOO0O0OO0O :#line:1851
                    if len (O0OOO000OO00O0000 ['cedents_struct']['cond'])>0 :#line:1852
                        OO0O0OO0O0000O000 =O0OOO000OO00O0000 ['cedents_str']['cond']#line:1853
                        OOO0O000OOOO00O0O =" & "+O0OOO000OO00O0000 ['cedents_str']['cond']#line:1854
                O00000O0O0O0O0OO0 [0 ,1 ].set (title =OO0O0OO0O0000O000 )#line:1855
                if O0000OOOOO0O0OO0O :#line:1856
                    OOOOOO0OO000O00OO =self .result ["rules"][rule_id -1 ]['cedents_str']['ante']+OOO0O000OOOO00O0O #line:1857
                else :#line:1858
                    OOOOOO0OO000O00OO =self .result ["rules"][rule_id -1 ]['cedents_str']['cond']#line:1859
                O00000O0O0O0O0OO0 [0 ,0 ].set (title ="\n".join (wrap (OOOOOO0OO000O00OO ,30 )))#line:1860
                O0O0O0000OOO00OOO =self .result ["rules"][rule_id -1 ]['cedents_str']#line:1862
                OO0O0OO0O0000O000 ="Condition : "+O0O0O0000OOO00OOO ['cond']#line:1863
                if O0000OOOOO0O0OO0O :#line:1864
                    OO0O0OO0O0000O000 =OO0O0OO0O0000O000 +"\nAntecedent : "+O0O0O0000OOO00OOO ['ante']#line:1865
                O000O0OOOO0OO00OO .suptitle (OO0O0OO0O0000O000 ,x =0 ,ha ='left',size ='small')#line:1866
                O000O0OOOO0OO00OO .tight_layout ()#line:1868
            else :#line:1869
                print ("Unsupported task type for rule details")#line:1870
                return #line:1871
            if filename is not None :#line:1872
                plt .savefig (filename =filename )#line:1873
            if show :#line:1874
                plt .show ()#line:1875
            print ("")#line:1877
        else :#line:1878
            print ("No such rule.")#line:1879
    def get_rulecount (self ):#line:1881
        """
        Gets number of rules.
        :return: number of rules in the resultset
        :rtype: int
        """#line:1886
        if not (self ._is_calculated ()):#line:1887
            print ("ERROR: Task has not been calculated.")#line:1888
            return #line:1889
        return len (self .result ["rules"])#line:1890
    def get_fourfold (self ,rule_id ,order =0 ):#line:1892
        """
        Gets a fourfold table for a specified rule.
        :param int rule_id: identification of the rule (rule number)
        :param int order: order of the fourfold table to be returned where more than one fourfold table is available (used for SD4ft-Miner, possible values are 1 and 2)
        :return: fourfold table as array of four integers
        :rtype: list
        """#line:1899
        if not (self ._is_calculated ()):#line:1900
            print ("ERROR: Task has not been calculated.")#line:1901
            return #line:1902
        if (rule_id <=len (self .result ["rules"])):#line:1903
            if self .result ['taskinfo']['task_type']=="4ftMiner":#line:1904
                OO0OO0OOO00O0000O =self .result ["rules"][rule_id -1 ]#line:1905
                return OO0OO0OOO00O0000O ['params']['fourfold']#line:1906
            elif self .result ['taskinfo']['task_type']=="CFMiner":#line:1907
                print ("Error: fourfold for CFMiner is not defined")#line:1908
                return None #line:1909
            elif self .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1910
                OO0OO0OOO00O0000O =self .result ["rules"][rule_id -1 ]#line:1911
                if order ==1 :#line:1912
                    return OO0OO0OOO00O0000O ['params']['fourfold1']#line:1913
                if order ==2 :#line:1914
                    return OO0OO0OOO00O0000O ['params']['fourfold2']#line:1915
                print ("Error: for SD4ft-Miner, you need to provide order of fourfold table in order= parameter (valid values are 1,2).")#line:1916
                return None #line:1917
            else :#line:1918
                print ("Unsupported task type for rule details")#line:1919
        else :#line:1920
            print ("No such rule.")#line:1921
    def get_hist (self ,rule_id ,fullCond =True ):#line:1923
        """
        Gets a histogram for the specified rule.
        :param int rule_id: identification of the rule (rule number)
        :param bool fullCond: (applicable for UIC Miner only) when True, show full histogram (given only by condition), when False, histogram given by condition and antecedent is shown
        :return: histogram as array of integers with length of unique values of the target variable
        :rtype: list
        """#line:1930
        if not (self ._is_calculated ()):#line:1931
            print ("ERROR: Task has not been calculated.")#line:1932
            return #line:1933
        if (rule_id <=len (self .result ["rules"])):#line:1934
            if self .result ['taskinfo']['task_type']=="CFMiner":#line:1935
                OO00O0OOOOOOOO0OO =self .result ["rules"][rule_id -1 ]#line:1936
                return OO00O0OOOOOOOO0OO ['params']['hist']#line:1937
            elif self .result ['taskinfo']['task_type']=="UICMiner":#line:1938
                OO00O0OOOOOOOO0OO =self .result ["rules"][rule_id -1 ]#line:1939
                OOO0OO0O00OOOO000 =None #line:1940
                if fullCond :#line:1941
                    OOO0OO0O00OOOO000 =OO00O0OOOOOOOO0OO ['params']['hist_cond']#line:1942
                else :#line:1943
                    OOO0OO0O00OOOO000 =OO00O0OOOOOOOO0OO ['params']['hist']#line:1944
                return OOO0OO0O00OOOO000 #line:1945
            elif self .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1946
                print ("Error: SD4ft-Miner has no histogram")#line:1947
                return None #line:1948
            elif self .result ['taskinfo']['task_type']=="4ftMiner":#line:1949
                print ("Error: 4ft-Miner has no histogram")#line:1950
                return None #line:1951
            else :#line:1952
                print ("Unsupported task type for rule details")#line:1953
        else :#line:1954
            print ("No such rule.")#line:1955
    def get_hist_cond (self ,rule_id ):#line:1958
        """
        Gets a histogram on a full dataset (given by condition in case of UIC Miner)
        :param rule_id: identification of the rule (rule number)
        :return: histogram as array of integers with length of unique values of the target variable
        :rtype: list
        """#line:1964
        if not (self ._is_calculated ()):#line:1965
            print ("ERROR: Task has not been calculated.")#line:1966
            return #line:1967
        if (rule_id <=len (self .result ["rules"])):#line:1969
            if self .result ['taskinfo']['task_type']=="UICMiner":#line:1970
                O000OOOO00O0OOO00 =self .result ["rules"][rule_id -1 ]#line:1971
                return O000OOOO00O0OOO00 ['params']['hist_cond']#line:1972
            elif self .result ['taskinfo']['task_type']=="CFMiner":#line:1973
                O000OOOO00O0OOO00 =self .result ["rules"][rule_id -1 ]#line:1974
                return O000OOOO00O0OOO00 ['params']['hist']#line:1975
            elif self .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1976
                print ("Error: SD4ft-Miner has no histogram")#line:1977
                return None #line:1978
            elif self .result ['taskinfo']['task_type']=="4ftMiner":#line:1979
                print ("Error: 4ft-Miner has no histogram")#line:1980
                return None #line:1981
            else :#line:1982
                print ("Unsupported task type for rule details")#line:1983
        else :#line:1984
            print ("No such rule.")#line:1985
    def get_quantifiers (self ,rule_id ,order =0 ):#line:1987
        """
        Gets a list of all quantifiers available for the rule


        :param int rule_id: identification of the rule (rule number)
        :param int order: (depreciated; kept for compatibility for a limited time)
        :return: dictionary with quantifiers and their values
        :rtype: list
        """#line:1996
        if not (self ._is_calculated ()):#line:1997
            print ("ERROR: Task has not been calculated.")#line:1998
            return None #line:1999
        if (rule_id <=len (self .result ["rules"])):#line:2001
            OO00O0O0OOOO000OO =self .result ["rules"][rule_id -1 ]#line:2002
            if self .result ['taskinfo']['task_type']=="4ftMiner":#line:2003
                return OO00O0O0OOOO000OO ['params']#line:2004
            elif self .result ['taskinfo']['task_type']=="CFMiner":#line:2005
                return OO00O0O0OOOO000OO ['params']#line:2006
            elif self .result ['taskinfo']['task_type']=="SD4ftMiner":#line:2007
                return OO00O0O0OOOO000OO ['params']#line:2008
            else :#line:2009
                print ("Unsupported task type for rule details")#line:2010
        else :#line:2011
            print ("No such rule.")#line:2012
    def get_varlist (self ):#line:2014
        """
        Gets a list of variables in the processed dataset
        :return [str]: array of variable names
        """#line:2018
        return self .result ["datalabels"]["varname"]#line:2020
    def get_category_names (self ,varname =None ,varindex =None ):#line:2022
        """
        Gets a list of category names for a required variable. The variable can be specified either by name or the index in variable list. Either varname or varindex must be specified.
        :param str varname: name of the variable
        :param int varindex: index of the variable
        :return: list of category names for a required variable
        :rtype: list
        """#line:2029
        OO000OOOO00000O00 =0 #line:2030
        if varindex is not None :#line:2031
            if OO000OOOO00000O00 >=0 &OO000OOOO00000O00 <len (self .get_varlist ()):#line:2032
                OO000OOOO00000O00 =varindex #line:2033
            else :#line:2034
                print ("Error: no such variable.")#line:2035
                return #line:2036
        if (varname is not None ):#line:2037
            OO00OOOOOO0OO0OO0 =self .get_varlist ()#line:2038
            OO000OOOO00000O00 =OO00OOOOOO0OO0OO0 .index (varname )#line:2039
            if OO000OOOO00000O00 ==-1 |OO000OOOO00000O00 <0 |OO000OOOO00000O00 >=len (self .get_varlist ()):#line:2040
                print ("Error: no such variable.")#line:2041
                return #line:2042
        return self .result ["datalabels"]["catnames"][OO000OOOO00000O00 ]#line:2043
    def print_data_definition (self ):#line:2045
        """
        Prints how CleverMiner understands categorical pandas dataset to be processed. Shows a list of variabes with number of categories for each variable.
        """#line:2048
        O0O0O0000OO000O0O =self .get_varlist ()#line:2049
        print (f"Dataset has {len(O0O0O0000OO000O0O)} variables.")#line:2050
        for O0OO00OOO000O0OOO in O0O0O0000OO000O0O :#line:2051
            O0OO00O0OOOOO000O =self .get_category_names (O0OO00OOO000O0OOO )#line:2052
            O000OO0O0OO0O00OO =""#line:2053
            for OOOOOO0OOOOOO00OO in O0OO00O0OOOOO000O :#line:2054
                O000OO0O0OO0O00OO =O000OO0O0OO0O00OO +str (OOOOOO0OOOOOO00OO )+" "#line:2055
            O000OO0O0OO0O00OO =O000OO0O0OO0O00OO [:-1 ]#line:2056
            print (f"Variable {O0OO00OOO000O0OOO} has {len(O0OO00O0OOOOO000O)} categories: {O000OO0O0OO0O00OO}")#line:2057
    def _is_calculated (self ):#line:2059
        """
        Internal routine.

        :return bool: True if task has been calculated, False otherwise
        """#line:2064
        O000O000O00OO0OOO =False #line:2065
        if 'taskinfo'in self .result :#line:2066
            O000O000O00OO0OOO =True #line:2067
        return O000O000O00OO0OOO #line:2068
    def get_version_string (self ):#line:2071
        """
        Gets a version string for CleverMiner package.

        :return str: version number
        """#line:2076
        return self .version_string #line:2077
