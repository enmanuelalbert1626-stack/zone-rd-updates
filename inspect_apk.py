"""Extract the real Android version before publishing an update manifest."""
import struct,zipfile,json,hashlib,pathlib,argparse
def inspect(path):
 with zipfile.ZipFile(path) as z: data=z.read('AndroidManifest.xml')
 strings=[];pos=8;values={}
 while pos<len(data):
  kind,header,size=struct.unpack_from('<HHI',data,pos)
  if size<8 or pos+size>len(data):raise ValueError('Manifiesto Android inválido')
  if kind==1:
   count,styles,flags,start=struct.unpack_from('<4I',data,pos+8)
   def length8(p):
    n=data[p];return ((n&127)<<8|data[p+1],p+2) if n&128 else (n,p+1)
   def length16(p):
    n=struct.unpack_from('<H',data,p)[0];return ((n&32767)<<16|struct.unpack_from('<H',data,p+2)[0],p+4) if n&32768 else (n,p+2)
   for i in range(count):
    p=pos+start+struct.unpack_from('<I',data,pos+header+4*i)[0]
    if flags&256:_,p=length8(p);n,p=length8(p);s=data[p:p+n].decode('utf-8')
    else:n,p=length16(p);s=data[p:p+n*2].decode('utf-16-le')
    strings.append(s)
  elif kind==0x102 and strings[struct.unpack_from('<I',data,pos+20)[0]]=='manifest':
   start,stride,count=struct.unpack_from('<3H',data,pos+24)
   for i in range(count):
    a=pos+16+start+i*stride;name=strings[struct.unpack_from('<I',data,a+4)[0]];typ=data[a+15];value=struct.unpack_from('<I',data,a+16)[0]
    values[name]=strings[value] if typ==3 else value
   break
  pos+=size
 package=values.get('package');code=values.get('versionCode');name=values.get('versionName')
 if package!='com.samceas.zonebrasil.rdtest' or not isinstance(code,int) or code<1:raise ValueError('El APK no corresponde al canal ZONE RD')
 digest=hashlib.sha256()
 with open(path,'rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):digest.update(chunk)
 return {'package_name':package,'latest_version_code':code,'version_name':name,'size':pathlib.Path(path).stat().st_size,'sha256':digest.hexdigest()}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('apk');p.add_argument('--url',required=True);p.add_argument('--mandatory',choices=['true','false'],default='true');p.add_argument('--message',required=True);p.add_argument('--output',default='docs/version.json');a=p.parse_args()
 result=inspect(a.apk);previous=json.loads(pathlib.Path(a.output).read_text());latest=result['latest_version_code']
 minimum=latest if a.mandatory=='true' else previous['min_supported_version_code']
 if minimum>latest:raise ValueError('Una publicación opcional no puede reducir la versión por debajo del mínimo activo')
 if not a.url.startswith('https://github.com/enmanuelalbert1626-stack/zone-rd-updates/releases/download/'):raise ValueError('Enlace fuera del canal oficial')
 document={'schema':1,'package_name':result['package_name'],'latest_version_code':latest,'min_supported_version_code':minimum,'version_name':result['version_name'],'message':a.message,'apk':{'url':a.url,'sha256':result['sha256'],'size':result['size']}}
 pathlib.Path(a.output).write_text(json.dumps(document,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('Versión publicada:',latest,'Mínima:',minimum)
