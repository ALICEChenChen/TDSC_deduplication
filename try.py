
# import hashlib
import hmac
def ORE_kGen():
    sk='infocom'.encode('utf-8')
    return sk

def ORE_Enc(PID,sk):
    m = "{0:b}".format(PID).zfill(16)
    u = m[0]
    for i in range(1, len(m)):
        hashm = hmac.new(sk, m[0:i].encode('utf-8'), digestmod='MD5').digest()
        intnum = int.from_bytes(hashm, byteorder='big', signed=False)
        u1 = (intnum + int(m[i])) % 3
        u = u + str(u1)
    return u

def ORE_Cmp(c1,c2):
    final=0
    for i in range(len(c1)):
        u1=int(c1[i])
        u2=int(c2[i])
        if u1==u2:
            continue
        if (u1+1)%3==u2%3:
            final=1  #u1<u2
            break
        if (u1-1)%3==u2%3:
            final = 2  #u1 > u2
            break
    return final





sk=ORE_kGen()
c1=ORE_Enc(121,sk)
c2=ORE_Enc(121,sk)
result=ORE_Cmp(c1,c2)
print(result)