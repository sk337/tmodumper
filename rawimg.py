import png
from io import BytesIO

def rawimgtopng(data, f):
  fh=BytesIO(data)
  def readColor(fh):
    color = fh.read(4)
    t=(color[0],color[1],color[2], color[3])
    return t
  def readInt32(fh):
    return int.from_bytes(fh.read(4),'little',signed=True)
  version = readInt32(fh)
  width = readInt32(fh)
  height = readInt32(fh)
  pngArry=[]
  for y in range(height):
    row=()
    for x in range(width):
      row=row+readColor(fh)
    pngArry.append(row)
  w=png.Writer(width, height, greyscale=False, alpha=True)
  w.write(f, pngArry)