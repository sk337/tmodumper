import hashlib
import zlib
import os
import rawimg
import math

if not os.path.isdir('out'):
  os.mkdir('out')

def readStr(fh):
  def decode_from_7bit(data):
    """
    Decode 7-bit encoded int from str data
    """
    result = 0
    for index, char in enumerate(data):
        byte_value = char
        result |= (byte_value & 0x7f) << (7 * index)
        if byte_value & 0x80 == 0:
            break
    return result

  strlen = decode_from_7bit(fh.read(1))
  
  return fh.read(strlen).decode()

def readUInt32(fh):
  return int.from_bytes(fh.read(4),'little')
def readInt32(fh):
  return int.from_bytes(fh.read(4),'little',signed=True)
with open("CalamityMod.tmod", 'rb') as fh:
  sig=fh.read(4)
  if sig!=b'TMOD':
    print('invalid sig')
    exit()
  version = readStr(fh)
  print("TMLversion: "+version)
  hashb = fh.read(20)
  hash=""
  for i in hashb:
    i=hex(i)
    if len(i) ==3:
      hash+="0"+i[2]
    else:
      hash+=i[2:]
  print("hash: "+hash)
  sig=fh.read(256)
  length=readUInt32(fh)
  ret = fh.tell()
  fileHash=hashlib.sha1(fh.read(length)).hexdigest()
  hashMatch= hash==fileHash
  print("ComputedHash: "+ fileHash)
  print("hashMatches: "+str(hashMatch))
  fh.seek(ret)
  modName=readStr(fh)
  print("modName: "+modName)
  modVersion=readStr(fh)
  print("modVersion: "+modVersion)
  fileCount=readInt32(fh)
  print("fileCount: "+ str(fileCount))
  print("decompressing Files...")
  inum=1
  idct=[]
  for i in range(fileCount):
    name=readStr(fh)
    uncompressed=readUInt32(fh)
    compressed=readUInt32(fh)
    # print(f"file {i+1}:")
    # print(f"  name+path: {name}") 
    # print(f"  uncompressedSize: {uncompressed}")
    # print(f"  compressedSize: {compressed}")
    idct.append({"name": name, "size": compressed, "unsize": uncompressed})
  for i in idct:

    path = i['name'].split('/')[:-1]
    # print("making dir for " + i['name'].split('/')[-1])
    mdir="out/"
    for e in path:
      if not os.path.isdir(mdir+e):
        os.mkdir(mdir+e)
      mdir+=e+'/'
    if i['name'].split('/')[-1].split('.')[-1]!='rawimg':
      with open("out/"+i['name'], 'wb') as f:
        if i['size']!=i['unsize']:
          uc=zlib.decompress(fh.read(i['size']), -15)
        else:
          f.write(fh.read(i['size']))
    else:
      print(f"converting image {inum}/{fileCount} ({math.ceil((inum/fileCount)*100*100)/100}%)")
      if i['size']!=i['unsize']:
        uc=zlib.decompress(fh.read(i['size']), -15)
        with open("out/"+'.'.join(i['name'].split('.')[:-1])+".png", 'wb') as f:
          rawimg.rawimgtopng(uc, f)
      else:
        with open("out/"+'.'.join(i['name'].split('.')[:-1])+".png", 'wb') as f:
          rawimg.rawimgtopng(fh.read(i['size']), f)
    inum+=1

  print("decompressed all files")

        
      