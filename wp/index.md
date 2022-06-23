# 在buuoj的刷题记录


## [rev][GKCTF 2021]QQQQT

exeinfope扫一下，有Enigma Virtual Box壳，搜索enigma Virtual Box unpacker，得到https://lifeinhex.com/tag/unpacker/

可以查看按钮监听事件，找到

```asm
.rdata:004044FC ??_7MainWindow@@6B@ dd offset sub_401A90
.rdata:004044FC                                         ; DATA XREF: main+3D↑o
.rdata:004044FC                                         ; sub_401120+8↑o ...
.rdata:00404500                 dd offset sub_401B10
.rdata:00404504                 dd offset sub_401AB0
.rdata:00404508                 dd offset loc_401180
.rdata:0040450C                 dd offset ?event@QMainWindow@@MAE_NPAVQEvent@@@Z ; QMainWindow::event(QEvent *)
.rdata:00404510                 dd offset ?eventFilter@QObject@@UAE_NPAV1@PAVQEvent@@@Z ; QObject::eventFilter(QObject *,QEvent *)
.rdata:00404514                 dd offset ?timerEvent@QObject@@MAEXPAVQTimerEvent@@@Z ; QObject::timerEvent(QTimerEvent *)
.rdata:00404518                 dd offset ?childEvent@QObject@@MAEXPAVQChildEvent@@@Z ; QObject::childEvent(QChildEvent *)
.rdata:0040451C                 dd offset ?customEvent@QObject@@MAEXPAVQEvent@@@Z ; QObject::customEvent(QEvent *)
.rdata:00404520                 dd offset ?connectNotify@QObject@@MAEXABVQMetaMethod@@@Z ; QObject::connectNotify(QMetaMethod const &)
.rdata:00404524                 dd offset ?disconnectNotify@QObject@@MAEXABVQMetaMethod@@@Z ; QObject::disconnectNotify(QMetaMethod const &)
.rdata:00404528                 dd offset ?setVisible@QWidget@@UAEX_N@Z ; QWidget::setVisible(bool)
.rdata:0040452C                 dd offset ?sizeHint@QWidget@@UBE?AVQSize@@XZ ; QWidget::sizeHint(void)
.rdata:00404530                 dd offset ?minimumSizeHint@QWidget@@UBE?AVQSize@@XZ ; QWidget::minimumSizeHint(void)
.rdata:00404534                 dd offset ?heightForWidth@QWidget@@UBEHH@Z ; QWidget::heightForWidth(int)
```
在三个函数下断点，直到点击按钮时断下即可

查看主要加密函数，base58
```cpp
QLineEdit::text(*(_DWORD *)(this[6] + 4), v15);
  v25 = 0;
  QString::toLatin1(v15, v16);
  LOBYTE(v25) = 1;
  v18 = QByteArray::data((QByteArray *)v16);
  v23[0] = 0i64;
  v23[1] = 0i64;
  v24 = 0i64;
  strcpy(v22, "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz");
  v20 = 138 * strlen(v18) / 0x64;
  v13 = v20 + 1;
  v1 = 0;
  v21 = malloc(v20 + 1);
  v2 = v21;
  memset(v21, 0, v13);
  v3 = v18;
  v19 = (int)(v18 + 1);
  if ( strlen(v18) )
  {
    v4 = &v2[v20];
    v17 = v4;
    while ( 1 )
    {
      v19 = ((char)*v4 << 8) + v3[v1];
      v5 = v19 / 58;
      *v4 = v19 % 58;
      if ( v5 )
      {
        do
        {
          v6 = (char)*--v4;
          v7 = (v6 << 8) + v5;
          v19 = v7 / 58;
          *v4 = v7 % 58;
          v5 = v19;
        }
        while ( v19 );
        v4 = v17;
      }
      if ( ++v1 >= strlen(v18) )
        break;
      v3 = v18;
    }
    v2 = v21;
  }
  v8 = 0;
  if ( !*v2 )
  {
    do
      ++v8;
    while ( !v2[v8] );
  }
  v9 = v20;
  if ( v8 <= v20 )
  {
    v10 = v2 - (_BYTE *)v23;
    do
    {
      v11 = (char *)v23 + v8++;
      *v11 = v22[(char)v11[v10]];
    }
    while ( v8 <= v9 );
  }
  if ( !qstrcmp((const char *)v23, "56fkoP8KhwCf3v7CEz") )
  {
    if ( v18 )
      v12 = strlen(v18);
    else
      v12 = -1;
    v21 = (_BYTE *)QString::fromAscii_helper(v18, v12);
    LOBYTE(v25) = 2;
    v20 = QString::fromAscii_helper("flag", 4);
    LOBYTE(v25) = 3;
    QMessageBox::warning(this, &v20, &v21, 1024, 0);
    QString::~QString((QString *)&v20);
    QString::~QString((QString *)&v21);
  }
```
## [rev][GKCTF 2021]Crash

go程序https://github.com/sibears/IDAGolangHelper

第一阶段三重DES加密

```cpp
crypto_des_NewTripleDESCipher(a1, a2, a3, a10, a5, a6, a10, 24LL, a12);
```

有个json字符串储存key和iv
```asm
.noptrdata:0000000000608840 aKeyWelcometoth db '{',0Dh,0Ah          ; DATA XREF: .data:off_61E540↓o
.noptrdata:0000000000608840                 db '    "key": "WelcomeToTheGKCTF2021XXX",',0Dh,0Ah
.noptrdata:0000000000608840                 db '    "iv": "1Ssecret"',0Dh,0Ah
.noptrdata:0000000000608840                 db '}',0
```
key=WelcomeToTheGKCTF2021XXX iv=1Ssecret
比对位于
```cpp
runtime_memequal(a1, a2, v9, (unsigned int)&aOAwpjnnxmpzdnj, v10, v11);
```
结果应该是base64编码
```asm
o/aWPjNNxMPZDnJlNp0zK5+NLPC4Tv6kqdJqjkL0XkA=
```
解密得到
```87f645e9-b628-412f-9d7a-```

后面的代码必须查看汇编代码
```asm
.text:0000000000514770                 call    Encrypt_HashHex2 ; sha256
.text:0000000000514775                 mov     rax, [rsp+78h+var_60]
.text:000000000051477A                 mov     rcx, [rsp+78h+var_58]
.text:000000000051477F                 nop
.text:0000000000514780                 cmp     rcx, 40h ; '@'
.text:0000000000514784                 jz      short loc_514798
.text:0000000000514786
.text:0000000000514786 loc_514786:                             ; CODE XREF: main_check+137↓j
.text:0000000000514786                 mov     [rsp+78h+arg_10], 0
.text:000000000051478E                 mov     rbp, [rsp+78h+var_8]
.text:0000000000514793                 add     rsp, 78h
.text:0000000000514797                 retn
.text:0000000000514798 ; ---------------------------------------------------------------------------
.text:0000000000514798
.text:0000000000514798 loc_514798:                             ; CODE XREF: main_check+104↑j
.text:0000000000514798                 mov     [rsp+78h+var_78], rax
.text:000000000051479C                 lea     rax, a6e2b55c78937d6 ; "6e2b55c78937d63490b4b26ab3ac3cb54df4c5c"...
.text:00000000005147A3                 mov     [rsp+78h+var_70], rax
.text:00000000005147A8                 mov     [rsp+78h+var_68], rcx
.text:00000000005147AD                 call    runtime_memequal
.text:00000000005147B2                 cmp     byte ptr [rsp+78h+var_60], 0
.text:00000000005147B7                 jz      short loc_514786
.text:00000000005147B9                 mov     rdx, [rsp+78h+len]
.text:00000000005147C1                 cmp     rdx, 26h ; '&'
.text:00000000005147C5                 jb      loc_5148E8
.text:00000000005147CB                 lea     rax, [rsp+78h+var_28]
.text:00000000005147D0                 mov     [rsp+78h+var_78], rax
.text:00000000005147D4                 mov     rax, [rsp+78h+input2]
.text:00000000005147DC                 lea     rcx, [rax+22h]
.text:00000000005147E0                 mov     [rsp+78h+var_70], rcx
.text:00000000005147E5                 mov     [rsp+78h+var_68], 4
.text:00000000005147EE                 call    runtime_stringtoslicebyte
.text:00000000005147F3                 mov     rax, [rsp+78h+var_60]
.text:00000000005147F8                 mov     rcx, [rsp+78h+var_58]
.text:00000000005147FD                 mov     rdx, [rsp+78h+var_50]
.text:0000000000514802                 mov     [rsp+78h+var_78], rax
.text:0000000000514806                 mov     [rsp+78h+var_70], rcx
.text:000000000051480B                 mov     [rsp+78h+var_68], rdx
.text:0000000000514810                 call    Encrypt_HashHex5 ； sha512
.text:0000000000514815                 mov     rax, [rsp+78h+var_60]
.text:000000000051481A                 mov     rcx, [rsp+78h+var_58]
.text:000000000051481F                 nop
.text:0000000000514820                 cmp     rcx, 80h
.text:0000000000514827                 jz      short loc_51483B
.text:0000000000514829
.text:0000000000514829 loc_514829:                             ; CODE XREF: main_check+1DA↓j
.text:0000000000514829                 mov     [rsp+78h+arg_10], 0
.text:0000000000514831                 mov     rbp, [rsp+78h+var_8]
.text:0000000000514836                 add     rsp, 78h
.text:000000000051483A                 retn
.text:000000000051483B ; ---------------------------------------------------------------------------
.text:000000000051483B
.text:000000000051483B loc_51483B:                             ; CODE XREF: main_check+1A7↑j
.text:000000000051483B                 mov     [rsp+78h+var_78], rax
.text:000000000051483F                 lea     rax, a6500fe72abcab6 ; "6500fe72abcab63d87f213d2218b0ee086a1828"...
.text:0000000000514846                 mov     [rsp+78h+var_70], rax
.text:000000000051484B                 mov     [rsp+78h+var_68], rcx
.text:0000000000514850                 call    runtime_memequal
.text:0000000000514855                 cmp     byte ptr [rsp+78h+var_60], 0
.text:000000000051485A                 jz      short loc_514829
.text:000000000051485C                 mov     rdx, [rsp+78h+len]
.text:0000000000514864                 cmp     rdx, 2Ah ; '*'
.text:0000000000514868                 jb      short loc_5148DE
.text:000000000051486A                 mov     rax, [rsp+78h+input2]
.text:0000000000514872                 add     rax, 26h ; '&'
.text:0000000000514876                 mov     [rsp+78h+var_78], rax
.text:000000000051487A                 mov     [rsp+78h+var_70], 4
.text:0000000000514883                 call    main_hash ; md5
.text:0000000000514888                 mov     rax, [rsp+78h+var_60]
.text:000000000051488D                 mov     rcx, [rsp+78h+var_68]
.text:0000000000514892                 cmp     rax, 20h ; ' '
.text:0000000000514896                 jz      short loc_5148AA
.text:0000000000514898
.text:0000000000514898 loc_514898:                             ; CODE XREF: main_check+24A↓j
.text:0000000000514898                 mov     [rsp+78h+arg_10], 0
.text:00000000005148A0                 mov     rbp, [rsp+78h+var_8]
.text:00000000005148A5                 add     rsp, 78h
.text:00000000005148A9                 retn
.text:00000000005148AA ; ---------------------------------------------------------------------------
.text:00000000005148AA
.text:00000000005148AA loc_5148AA:                             ; CODE XREF: main_check+216↑j
.text:00000000005148AA                 mov     [rsp+78h+var_78], rcx
.text:00000000005148AE                 lea     rcx, byte_54E0D6
.text:00000000005148B5                 mov     [rsp+78h+var_70], rcx
.text:00000000005148BA                 mov     [rsp+78h+var_68], rax
.text:00000000005148BF                 nop
.text:00000000005148C0                 call    runtime_memequal
.text:00000000005148C5                 cmp     byte ptr [rsp+78h+var_60], 0
.text:00000000005148CA                 jz      short loc_514898
.text:00000000005148CC                 mov     [rsp+78h+arg_10], 1
.text:00000000005148D4                 mov     rbp, [rsp+78h+var_8]
.text:00000000005148D9                 add     rsp, 78h
.text:00000000005148DD                 retn
```
使用python穷举一下，itertools很快

```python
from Crypto.Cipher import DES3

des=DES3.new(key=b'WelcomeToTheGKCTF2021XXX',iv=b'1Ssecret',mode=DES3.MODE_CBC)
import base64
import hashlib
import itertools
r=des.decrypt(base64.b64decode(b'o/aWPjNNxMPZDnJlNp0zK5+NLPC4Tv6kqdJqjkL0XkA='))
print(len(r),r)

sha256_str='6e2b55c78937d63490b4b26ab3ac3cb54df4c5ca7d60012c13d2d1234a732b74'
sha512_str='6500fe72abcab63d87f213d2218b0ee086a1828188439ca485a1a40968fd272865d5ca4d5ef5a651270a52ff952d955c9b757caae1ecce804582ae78f87fa3c9c6858e06b70404e9cd9e3ecb662395b4429c648139053fb521f828af606b4d3dbaa14b5e77efe75928fe1dc127a2ffa8de3348b3c1856a429bf97e7e31c2e5bd66051953eb9618e1c9a1f929a21a0b68540eea2da725b99b315f3b8b489918ef109e156193951ec7e937b1652c0bd3bb1bf073573df883d2c34f1ef451fd46b503f0011839296a789a3bc0045c8a5fb42c7d1bd998f54449579b446817afbd17273e662c97ee72995ef42640c550b9013fad0761353c7086a272c24088be94769fd166506864797660130609714981900799081393217269435300143305409394463459185543183397656052122559640661454554977296311391480858037121987999716643812574028291115057151686479766013060971498190079908139321726943530014330540939446345918554318339765539424505774633321719753296399637136332111386476861244038034037280889270700544900010203040506070809101112131415161718192021222324252627282930313233343536373839404142434445464748495051525354555657585960616263646566676869707172737475767778798081828384858687888990919293949596979899'[:128]
md5_str='ff6e2fd78aca4736037258f0ede4ecf0'
print(hashlib.sha512(b'00').hexdigest())

tab='0123456789abcdef'
sha256_ok=False
sha512_ok=False
md5_ok=False
for i in itertools.product(tab,repeat=4):
    s=''.join(i).encode()
    if not sha256_ok and hashlib.sha256(s).hexdigest()==sha256_str:
        print('sha256:',s)
        sha256_ok=True
    if not sha512_ok and hashlib.sha512(s).hexdigest()==sha512_str:
        print('sha512:',s)
        sha512_ok=True
    if not md5_ok and hashlib.md5(s).hexdigest()==md5_str:
        print('md5:',s)
        md5_ok=True
    if sha256_ok and sha512_ok and md5_ok:break
# GKCTF{87f645e9-b628-412f-9d7a-e402f20af940}
```

## [rev][XNUCA2018]Code_Interpreter

虚拟机，解析之后使用z3即可

```python
import struct

def decompile(code):

    ip=0
    esp=2
    data_seg=[0]*256
    regs=[0]*256
    # regs[7]=0,[6]=2,[5]=0
    while ip<len(code):
        op=code[ip]
        s=''
        if op==0:
            print(len(code)-ip)
            break
        elif op==1:
            data_seg[esp]=struct.unpack('<I',code[ip+1:ip+5])[0]
            esp+=1
            s='data_seg[%d]=0x%x'%(esp,struct.unpack('<I',code[ip+1:ip+5])[0])
            ip+=5
        elif op==2:
            esp-=1
            s='esp-=1'
            ip+=1
        elif op==3:
            regs[code[ip+1]]+=regs[code[ip+2]]
            s='regs[%d]+=regs[%d]'%(code[ip+1],code[ip+2])
            ip+=3
        elif op==4:
            regs[code[ip+1]]-=code[ip+2]
            s='regs[%d]-=regs[%d]'%(code[ip+1],code[ip+2])
            ip+=3
        elif op==5:
            regs[code[ip+1]]*=code[ip+2]
            s='regs[%d]*=%d'%(code[ip+1],code[ip+2])
            ip+=3
        elif op==6:
            regs[code[ip+1]]>>=code[ip+2]
            s='regs[%d]>>=%d'%(code[ip+1],code[ip+2])
            ip+=3
        elif op==7:
            regs[code[ip+1]]=regs[code[ip+2]]
            s='regs[%d]=regs[%d]'%(code[ip+1],code[ip+2])
            ip+=3
        elif op==8:
            regs[code[ip+1]]=data_seg[code[ip+2]]
            s='regs[%d]+=data_seg[regs[7]+%d]'%(code[ip+1],code[ip+2])
            ip+=3
        elif op==9:
            regs[code[ip+1]]^=code[ip+2]
            s='regs[%d]^=regs[%d]'%(code[ip+1],code[ip+2])
            ip+=3
        elif op==10:
            regs[code[ip+1]]|=code[ip+2]
            s='regs[%d]|=regs[%d]'%(code[ip+1],code[ip+2])
            ip+=3
        else:
            print('error op code')
            exit(1)
        print('%x'%ip,s)
decompile(open('code','rb').read())

# regs[1]=0
from z3 import *
x,y,z=BitVec('x',32),BitVec('y',32),BitVec('z',32)

s=Solver()
s.add(
    ((x>>4)*21-z-0x1d7ecc6b)|
    ((z>>8)*3+y-0x6079797c)|
    ((x>>8)+y-0x5fbcbdbd)==0
)
s.add(x&0xff==94)
s.add(y&0xff0000==0x5E0000)
s.add(z&0xff==94)
print(s.check())

m=s.model()
print('X-NUCA{%x%x%x}'%(m[x].as_long(),m[y].as_long(),m[z].as_long()))
```

## [rev][WMCTF2020]easy_apk

前面的字符串是string_fog加密https://github.com/MegatronKing/StringFog

check逻辑在libnative-lib.so，Java层有一些反调试，Patch掉smali源码即可

查看JNI_OnLoad

```cpp
jint JNI_OnLoad(JavaVM *vm, void *reserved)
{
  //...

  v8 = *(_QWORD *)(_ReadStatusReg(ARM64_SYSREG(3, 3, 13, 0, 2)) + 40);
  if ( !(*vm)->GetEnv(vm, (void **)&v4, 65542LL) )
  {
    //...
    (*v4)->RegisterNatives(v4, v2, (const JNINativeMethod *)methods, 1LL);
  }
  return 65542;
}
```

method信息

```asm
.data:0000000000046008 methods         DCQ aCheck              ; DATA XREF: LOAD:0000000000002220↑o
.data:0000000000046008                                         ; .got:methods_ptr↑o
.data:0000000000046008                                         ; "check"
.data:0000000000046010                 DCQ aLjavaLangStrin     ; "(Ljava/lang/String;)Z"
.data:0000000000046018                 DCQ check
.data:0000000000046020                 DCQ __gxx_personality_v0
.data:0000000000046028                 EXPORT __cxa_terminate_handler
```

加密算法在10ce8，在此之前有几个反调试

```cpp
__int64 sub_DFD4()
{
  //...

  v5 = *(_QWORD *)(_ReadStatusReg(ARM64_SYSREG(3, 3, 13, 0, 2)) + 40);
  memcpy(dest, "/data/local/su", sizeof(dest));
  v0 = 0LL;
  while ( 1 )
  {
    v1 = v0 + 30;
    if ( v0 == 300 )
      break;
    v2 = fopen(&dest[v0], "r");
    v0 = v1;
    if ( v2 )
      return 1LL;
  }
  return 0LL;
}
```

查看su反调试。E074也有个反调试，似乎是读取某个特定文件

一旦检测到调试，则获取pid并kill

```cpp
if ( (unsigned int)sub_E074((__int64)input_3, (__int64)input_2) )
  {
    v8 = get_pid();
    kill_pid9(v8, 9);
  }
  if ( (check_su() & 1) != 0 )                  // check_su
  {
    v9 = get_pid();
    kill_pid9(v9, 9);
  }
```

因此可以patch掉kill逻辑

```asm
.text:000000000000D994 kill_pid9                               ; CODE XREF: sub_E260+150↓p
.text:000000000000D994                                         ; .text:000000000000E45C↓p ...
.text:000000000000D994 ; __unwind {
.text:000000000000D994                 RET
.text:000000000000D998 ; ---------------------------------------------------------------------------
.text:000000000000D998                 SVC             0
.text:000000000000D99C                 CMN             X0, #1,LSL#12
.text:000000000000D9A0                 CINV            X0, X0, HI
.text:000000000000D9A4                 B.HI            sub_10E94
.text:000000000000D9A8                 RET
.text:000000000000D9A8 ; } // starts at D994
```

然后查看加密算法10ce8，使用了一个常量序列```0x3E 0x72 0x5B 0x47 0xCA 0xE0 ...```，[搜索](https://www.google.com/search?q=0x3E+0x72+0x5B+0x47+0xCA+0xE0&oq=0x3E+0x72+0x5B+0x47+0xCA+0xE0&aqs=chrome..69i57.1435j0j7&client=ubuntu&sourceid=chrome&ie=UTF-8)一下，发现是ZUC祖冲之序列密码算法。既然是序列密码，既可以调试出秘钥和IV，也可以把明文改为密文输入

找到密文

```py
[0x17, 0x83, 0x1, 0x69, 0xd9, 0xd9, 0x0, 0x37, 0xe4, 0xac, 0x63, 0xbc, 0x7d, 0x8e, 0x4c, 0xc9, 0x6c, 0xc1, 0x95, 0x8d, 0xf4, 0xaa, 0xf2, 0x86, 0x96, 0xb8, 0xfc, 0x59, 0x19, 0xf0, 0x5d, 0x3a]
```

使用IDA调试，安装后还是闪退，说明还是有反调试，Java层已经patch好了，那么只有native层，几个加载函数init_proc和init_array。最后发现是illegalState异常，也就是说是打包问题

只能静态分析，发现E074是AES加密，有AES特征码

```cpp
__int64 __fastcall sub_E074(__int64 a1, __int64 a2)
{
  //...

  v23 = *(_QWORD *)(_ReadStatusReg(ARM64_SYSREG(3, 3, 13, 0, 2)) + 40);
  v22[0] = unk_293C4;
  v22[1] = unk_293D4;
  v4 = getpid();
  v5 = (char *)operator new[](0x14uLL);
  v19 = xmmword_29424;
  v20 = 0x8E0000008CLL;
  clear_nzero(v13, (__int64)&v19, 6);
  v6 = sub_DA24((int8x8_t *)v14, v4);
  strcat(v5, v13, v6);
  v18[0] = xmmword_293E4;
  *(_OWORD *)((char *)v18 + 12) = *(__int128 *)((char *)&xmmword_293E4 + 12);
  clear_nzero(v12, (__int64)v18, 7);
  strcat(v5, v5, v12);
  v7 = fopen(v5, "r");
  if ( !v7 )
    return 0;
  v8 = v7;
  v9 = set_ns(32LL);
  if ( feof(v8) )
    return 0;
  while ( 1 )
  {
    fgets(s, 128, v8);
    v16[1] = xmmword_29410;
    v17 = 106;
    v16[0] = xmmword_29400;
    clear_nzero(a2a, (__int64)v16, 9);
    if ( str_prifix_cmp(s, a2a) )               // 如果是前缀则返回str1，否则返回0
      break;
    if ( feof(v8) )
      return 0;
  }
  v10 = atoi(&s[10]);
  fclose(v8);
  AES((__int64)v22, (__int64)v9); // key init
  if ( *(_BYTE *)(a2 + 8) )
  {
    *(_BYTE *)(a2 + 8) = v10;
    sub_F8E0(a2, a1, v9); // encrypt
  }
  return v10;
}
```

TODO

## [web] [极客大挑战 2019]Http

首先查看源码或抓包，在卖鞋场那里找到了一个隐藏的按钮Secret.php

进入之后说需要从https://www.buuoj.Sycsecret.com访问，这里加一个Referer字段。referer常用的使用场景是统计流量来源。

然后说让用Syclover浏览器，就改UA的第一个为Syclover

最后是需要从本地访问，改X-Forwarded-For为127.0.0.1
