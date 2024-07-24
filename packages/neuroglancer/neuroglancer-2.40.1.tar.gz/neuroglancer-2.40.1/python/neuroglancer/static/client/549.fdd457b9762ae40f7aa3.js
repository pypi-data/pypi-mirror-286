const A=549,T=[549],C={2366:(R,h,l)=>{l.d(h,{R:()=>u});var a=l(4509),s=l(9808);/**
 * @license
 * Copyright 2019 Google Inc.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const t=3;async function u(o,n,f,e,r,i,m=a.fx){let _;for(let E=0;;){(0,a.Dq)(m),E>1&&await new Promise(p=>setTimeout(p,(0,s.JZ)(E-2))),_=await o.get(_,m);try{return await(0,s.Bk)(typeof n=="function"?n(_.credentials):n,r(_.credentials,f),e,m)}catch(p){if(p instanceof s.j$&&i(p,_.credentials)==="refresh"){if(++E===t)throw p;continue}throw p}}}},3551:(R,h,l)=>{l.d(h,{Y:()=>u});var a=l(2366),s=l(4509),t=l(9808);/**
 * @license
 * Copyright 2020 Google Inc.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function u(o,n,f,e,r=s.fx){return o===void 0?(0,t.Bk)(n,f,e,r):(0,a.R)(o,n,f,e,(i,m)=>{if(!i.accessToken)return m;const _=new Headers(m.headers);return _.set("Authorization",`${i.tokenType} ${i.accessToken}`),{...m,headers:_}},(i,m)=>{const{status:_}=i;if(_===401||_===403&&!m.accessToken)return"refresh";throw i instanceof Error&&m.email!==void 0&&(i.message+=`  (Using credentials for ${JSON.stringify(m.email)})`),i},r)}},957:(R,h,l)=>{l.d(h,{P:()=>a,y:()=>s});/**
 * @license
 * Copyright 2017 Google Inc.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const a="CredentialsProvider",s="CredentialsProvider.get"},6650:(R,h,l)=>{l.d(h,{Ve:()=>t,jj:()=>s});/**
 * @license
 * Copyright 2017 Google Inc.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class a{}class s extends a{static stringify(o){return`boss:volume:${o.baseUrl}/${o.collection}/${o.experiment}/${o.channel}/${o.resolution}/${o.encoding}`}}s.RPC_ID="boss/VolumeChunkSource";class t{static stringify(o){return`boss:mesh:${o.baseUrl}`}}t.RPC_ID="boss/MeshChunkSource"},2020:(R,h,l)=>{l.d(h,{CR:()=>t,Ip:()=>u,NV:()=>n,Rw:()=>e,Ve:()=>o,r7:()=>a,rl:()=>f});/**
 * @license
 * Copyright 2016 Google Inc.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */var a=(r=>(r[r.RAW=0]="RAW",r[r.JPEG=1]="JPEG",r[r.COMPRESSED_SEGMENTATION=2]="COMPRESSED_SEGMENTATION",r))(a||{});class s{}class t{}t.RPC_ID="brainmaps/VolumeChunkSource";class u{}u.RPC_ID="brainmaps/MultiscaleMeshSource";class o{}o.RPC_ID="brainmaps/MeshSource";class n{}n.RPC_ID="brainmaps/SkeletonSource";class f{}f.RPC_ID="brainmaps/Annotation";class e{}e.RPC_ID="brainmaps/AnnotationSpatialIndex"},5990:(R,h,l)=>{l.d(h,{D:()=>s,j:()=>a});/**
 * @license
 * Copyright 2016 Google Inc., 2023 Gergely Csucs
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */var a=(t=>(t[t.JPG=0]="JPG",t[t.JPEG=1]="JPEG",t[t.PNG=2]="PNG",t))(a||{});class s{}s.RPC_ID="deepzoom/ImageTileSource"},8820:(R,h,l)=>{l.d(h,{NV:()=>u,Ve:()=>o,jj:()=>t,r7:()=>a});/**
 * @license
 * Copyright 2016 Google Inc.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */var a=(n=>(n[n.JPEG=0]="JPEG",n[n.RAW=1]="RAW",n[n.COMPRESSED_SEGMENTATION=2]="COMPRESSED_SEGMENTATION",n[n.COMPRESSED_SEGMENTATIONARRAY=3]="COMPRESSED_SEGMENTATIONARRAY",n))(a||{});class s{}class t extends s{}t.RPC_ID="dvid/VolumeChunkSource";class u extends s{}u.RPC_ID="dvid/SkeletonSource";class o extends s{}o.RPC_ID="dvid/MeshSource"},5926:(R,h,l)=>{l.d(h,{j:()=>s,r:()=>a});/**
 * @license
 * Copyright 2019 Google Inc.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */var a=(t=>(t[t.RAW=0]="RAW",t[t.GZIP=1]="GZIP",t[t.BLOSC=2]="BLOSC",t[t.ZSTD=3]="ZSTD",t))(a||{});class s{}s.RPC_ID="n5/VolumeChunkSource"},6435:(R,h,l)=>{l.d(h,{C:()=>s,Y:()=>a});/**
 * @license
 * Copyright 2016 Google Inc.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const a="nifti/getNiftiVolumeInfo";class s{}s.RPC_ID="nifti/VolumeChunkSource"},3819:(R,h,l)=>{l.d(h,{Ip:()=>f,NV:()=>e,Rw:()=>r,TV:()=>o,Ve:()=>t,Y1:()=>u,jj:()=>s,r7:()=>a,rl:()=>i,vq:()=>m});/**
 * @license
 * Copyright 2016 Google Inc.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */var a=(_=>(_[_.RAW=0]="RAW",_[_.JPEG=1]="JPEG",_[_.COMPRESSED_SEGMENTATION=2]="COMPRESSED_SEGMENTATION",_[_.COMPRESSO=3]="COMPRESSO",_[_.PNG=4]="PNG",_))(a||{});class s{}s.RPC_ID="precomputed/VolumeChunkSource";class t{}t.RPC_ID="precomputed/MeshSource";var u=(_=>(_[_.RAW=0]="RAW",_[_.GZIP=1]="GZIP",_))(u||{}),o=(_=>(_[_.IDENTITY=0]="IDENTITY",_[_.MURMURHASH3_X86_128=1]="MURMURHASH3_X86_128",_))(o||{});class n{}class f{}f.RPC_ID="precomputed/MultiscaleMeshSource";class e{}e.RPC_ID="precomputed/SkeletonSource";class r{}r.RPC_ID="precomputed/AnnotationSpatialIndexSource";class i{}i.RPC_ID="precomputed/AnnotationSource";class m{}m.RPC_ID="precomputed/IndexedSegmentPropertySource"},9063:(R,h,l)=>{l.d(h,{NV:()=>o,Ve:()=>u,jj:()=>t,r7:()=>a});/**
 * @license
 * Copyright 2016 Google Inc.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */var a=(n=>(n[n.JPEG=0]="JPEG",n[n.NPZ=1]="NPZ",n[n.RAW=2]="RAW",n))(a||{});class s{}class t extends s{}t.RPC_ID="python/VolumeChunkSource";class u extends s{}u.RPC_ID="python/MeshSource";class o extends s{}o.RPC_ID="python/SkeletonSource"},8997:(R,h,l)=>{l.d(h,{vc:()=>t});/**
 * @license
 * Copyright 2016 Google Inc.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class a{}class s extends a{}class t extends s{}t.RPC_ID="render/TileChunkSource"},6742:(R,h,l)=>{l.d(h,{j:()=>a});/**
 * @license
 * Copyright 2019 Google Inc.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class a{}a.RPC_ID="zarr/VolumeChunkSource"},2334:(R,h,l)=>{l.d(h,{L:()=>a});/**
 * @license
 * Copyright 2023 Google Inc.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */var a=(s=>(s[s.arrayToArray=0]="arrayToArray",s[s.arrayToBytes=1]="arrayToBytes",s[s.bytesToBytes=2]="bytesToBytes",s))(a||{})},9254:(R,h,l)=>{l.d(h,{_:()=>t});/**
 * @license
 * Copyright 2016 Google Inc.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const a=3432918353,s=461845907;function t(u,o){return o>>>=0,u>>>=0,o=Math.imul(o,a)>>>0,o=(o<<15|o>>>17)>>>0,o=Math.imul(o,s)>>>0,u=(u^o)>>>0,u=(u<<13|u>>>19)>>>0,u=u*5+3864292196>>>0,u}},3708:(R,h,l)=>{l.d(h,{Of:()=>a,Pc:()=>o,Yo:()=>s,dI:()=>t,pi:()=>u});/**
 * @license
 * Copyright 2016 Google Inc.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const a="mesh/MeshLayer",s="mesh/MultiscaleMeshLayer",t="mesh/FragmentSource",u="mesh/MultiscaleFragmentSource";var o=(n=>(n[n.float32=0]="float32",n[n.uint10=1]="uint10",n[n.uint16=2]="uint16",n))(o||{})},4373:(R,h,l)=>{l.d(h,{l:()=>a});/**
 * @license
 * Copyright 2018 Google Inc.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const a="perspective_view/PerspectiveView"},3517:(R,h,l)=>{l.d(h,{Bh:()=>t,kg:()=>u,lG:()=>s,sC:()=>a});/**
 * @license
 * Copyright 2019 Google Inc.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const a="rendered_view.addLayer",s="rendered_view.removeLayer",t="SharedProjectionParameters",u="SharedProjectionParameters.changed"},6015:(R,h,l)=>{l.d(h,{Fe:()=>o,N3:()=>s,b7:()=>t,nG:()=>a});/**
 * @license
 * Copyright 2016 Google Inc.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const a="single_mesh/SingleMeshLayer",s="single_mesh/getSingleMeshInfo",t="";class u{}class o extends u{}o.RPC_ID="single_mesh/SingleMeshSource"},3786:(R,h,l)=>{l.d(h,{k:()=>a});/**
 * @license
 * Copyright 2016 Google Inc.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const a="skeleton/SkeletonLayer"},9459:(R,h,l)=>{l.d(h,{i:()=>t});var a=l(3038),s=l(147);/**
 * @license
 * Copyright 2016 Google Inc.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class t{constructor(o,n,f){this.size=a.eR.clone(o),this.transform=a.pB.clone(n),this.finiteRank=f;const e=a.pB.create(),r=s.DI(e,4,n,4,4);if(r===0)throw new Error("Transform is singular");this.invTransform=e,this.detTransform=r}toObject(){return{size:this.size,transform:this.transform,finiteRank:this.finiteRank}}static fromObject(o){return new t(o.size,o.transform,o.finiteRank)}globalToLocalSpatial(o,n){return a.eR.transformMat4(o,n,this.invTransform)}localSpatialVectorToGlobal(o,n){return(0,a.vs)(o,n,this.transform)}globalToLocalNormal(o,n){return(0,a.uD)(o,n,this.transform)}}},4104:(R,h,l)=>{l.d(h,{t:()=>a});/**
 * @license
 * Copyright 2017 Google Inc.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function a(s){let t=-1;return Object.assign(()=>{t===-1&&(t=requestAnimationFrame(()=>{t=-1,s()}))},{flush:()=>{t!==-1&&(t=-1,s())},cancel:()=>{t!==-1&&(cancelAnimationFrame(t),t=-1)}})}},9100:(R,h,l)=>{l.d(h,{I:()=>g});var a=l(4242),s=l(3206),t=l(8796);/**
 * @license
 * Copyright 2016 Google Inc.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const u=Symbol("disjoint_sets:rank"),o=Symbol("disjoint_sets:parent"),n=Symbol("disjoint_sets:next"),f=Symbol("disjoint_sets:prev");function e(P){let c=P,S=P[o];for(;S!==P;)P=S,S=P[o];for(P=c[o];S!==P;)c[o]=S,c=P,P=c[o];return S}function r(P,c){const S=P[u],d=c[u];return S>d?(c[o]=P,P):(P[o]=c,S===d&&(c[u]=d+1),c)}function i(P,c){const S=P[f],d=c[f];c[f]=S,S[n]=c,P[f]=d,d[n]=P}function*m(P){let c=P;do yield c,c=c[n];while(c!==P)}function _(P){P[o]=P,P[u]=0,P[n]=P[f]=P}const E=Symbol("disjoint_sets:min");function p(P){return P[o]===P}class g{constructor(){this.map=new Map,this.visibleSegmentEquivalencePolicy=new s.B0(a.y6.MIN_REPRESENTATIVE),this.generation=0}has(c){const S=c.toString();return this.map.get(S)!==void 0}get(c){const S=c.toString(),d=this.map.get(S);return d===void 0?c:e(d)[E]}isMinElement(c){const S=this.get(c);return S===c||t.R.equal(S,c)}makeSet(c){const S=c.toString(),{map:d}=this;let w=d.get(S);return w===void 0?(w=c.clone(),_(w),w[E]=w,d.set(S,w),w):e(w)}link(c,S){if(c=this.makeSet(c),S=this.makeSet(S),c===S)return!1;this.generation++;const d=r(c,S);i(c,S);const w=c[E],I=S[E],D=(this.visibleSegmentEquivalencePolicy.value&a.y6.MAX_REPRESENTATIVE)!==0;return d[E]=t.R.less(w,I)===D?I:w,!0}linkAll(c){for(let S=1,d=c.length;S<d;++S)this.link(c[0],c[S])}deleteSet(c){const{map:S}=this;let d=!1;for(const w of this.setElements(c))S.delete(w.toString()),d=!0;return d&&++this.generation,d}*setElements(c){const S=c.toString(),d=this.map.get(S);d===void 0?yield c:yield*m(d)}clear(){const{map:c}=this;return c.size===0?!1:(++this.generation,c.clear(),!0)}get size(){return this.map.size}*mappings(c=new Array(2)){for(const S of this.map.values())c[0]=S,c[1]=e(S)[E],yield c}*roots(){for(const c of this.map.values())p(c)&&(yield c)}[Symbol.iterator](){return this.mappings()}toJSON(){const c=new Array;for(const S of this.map.values())if(p(S)){const d=new Array;for(const w of m(S))d.push(w);d.sort(t.R.compare),c.push(d)}return c.sort((S,d)=>t.R.compare(S[0],d[0])),c.map(S=>S.map(d=>d.toString()))}}},8103:(R,h,l)=>{l.d(h,{K:()=>s});/**
 * @license
 * Copyright 2018 Google Inc.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const a=new Float32Array(1);function s(t){a[0]=t,t=a[0];for(let u=1;u<21;++u){const o=t.toPrecision(u);if(a[0]=parseFloat(o),a[0]===t)return o}return t.toString()}},4472:(R,h,l)=>{l.d(h,{A:()=>a});/**
 * @license
 * Copyright 2016 Google Inc.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const a=class{static insertAfter(s,t){const u=s.next0;t.next0=u,t.prev0=s,s.next0=t,u.prev0=t}static insertBefore(s,t){const u=s.prev0;t.prev0=u,t.next0=s,s.prev0=t,u.next0=t}static front(s){const t=s.next0;return t===s?null:t}static back(s){const t=s.prev0;return t===s?null:t}static pop(s){const t=s.next0,u=s.prev0;return t.prev0=u,u.next0=t,s.next0=null,s.prev0=null,s}static*iterator(s){for(let t=s.next0;t!==s;t=t.next0)yield t}static*reverseIterator(s){for(let t=s.prev0;t!==s;t=t.prev0)yield t}static initializeHead(s){s.next0=s.prev0=s}}},4704:(R,h,l)=>{l.d(h,{d:()=>t,e:()=>u});var a=l(2596),s=l(7900);/**
 * @license
 * Copyright 2016 Google Inc.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class t{constructor(){this.map=new Map}get(n,f){const{map:e}=this;let r=e.get(n);return r===void 0?(r=f(),r.registerDisposer(()=>{e.delete(n)}),e.set(n,r)):r.addRef(),r}}class u extends t{get(n,f){return typeof n!="string"&&(n=(0,s.JB)(n)),super.get(n,f)}getUncounted(n,f){return this.get(n,()=>new a.fL(f())).value}}},8795:(R,h,l)=>{l.d(h,{e:()=>a});/**
 * @license
 * Copyright 2019 Google Inc.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function a(s,t){return s<t?-1:s>t?1:0}},6703:(R,h,l)=>{l.d(h,{F:()=>t});var a=l(7900),s=l(4038);/**
 * @license
 * Copyright 2017 Google Inc.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class t{constructor(o,n,f=n){this.enumType=o,this.value_=n,this.defaultValue=f,this.changed=new s.IY}set value(o){this.value_!==o&&(this.value_=o,this.changed.dispatch())}get value(){return this.value_}reset(){this.value=this.defaultValue}restoreState(o){this.value=(0,a.sl)(o,this.enumType)}toJSON(){if(this.value_!==this.defaultValue)return this.enumType[this.value_].toLowerCase()}}},8796:(R,h,l)=>{l.d(h,{R:()=>n});/**
 * @license
 * Copyright 2016 Google Inc.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const a=new Uint32Array(2),s=4294967296,t=[];for(let f=2;f<=36;++f){const e=Math.floor(32/Math.log2(f)),r=f**e;let i=`^[0-${String.fromCharCode(48+Math.min(9,f-1))}`;f>10&&(i+=`a-${String.fromCharCode(97+f-11)}`,i+=`A-${String.fromCharCode(65+f-11)}`);const m=Math.ceil(64/Math.log2(f));i+=`]{1,${m}}$`;const _=new RegExp(i);t[f]={lowDigits:e,lowBase:r,pattern:_}}function u(f,e){f>>>=0,e>>>=0;const r=f&65535,i=f>>>16,m=e&65535,_=e>>>16;let p=(r*m>>>16)+i*m,g=p>>>16;p=(p&65535)+r*_,g+=p>>>16;let P=g>>>16;return g=(g&65535)+i*_,P+=g>>>16,((P&65535)<<16|g&65535)>>>0}const o=class M{constructor(e=0,r=0){this.low=e,this.high=r}clone(){return new M(this.low,this.high)}assign(e){this.low=e.low,this.high=e.high}toString(e=10){let r=this.low,i=this.high;if(i===0)return r.toString(e);i*=s;const{lowBase:m,lowDigits:_}=t[e],E=i%m;i=Number(BigInt(i)/BigInt(m)),r+=E,i+=Math.floor(r/m),r=r%m;const p=r.toString(e);return i.toString(e)+"0".repeat(_-p.length)+p}static less(e,r){return e.high<r.high||e.high===r.high&&e.low<r.low}static compare(e,r){return e.high-r.high||e.low-r.low}static equal(e,r){return e.low===r.low&&e.high===r.high}static min(e,r){return M.less(e,r)?e:r}static max(e,r){return M.less(e,r)?r:e}static random(){return crypto.getRandomValues(a),new M(a[0],a[1])}tryParseString(e,r=10){const{lowDigits:i,lowBase:m,pattern:_}=t[r];if(!_.test(e))return!1;if(e.length<=i)return this.low=parseInt(e,r),this.high=0,!0;const E=e.length-i,p=parseInt(e.substr(E),r),g=parseInt(e.substr(0,E),r);let P,c;if(m===s)P=g,c=p;else{const S=Math.imul(g,m)>>>0;P=u(g,m)+(Math.imul(Math.floor(g/s),m)>>>0),c=p+S,c>=s&&(++P,c-=s)}return c>>>0!==c||P>>>0!==P?!1:(this.low=c,this.high=P,!0)}parseString(e,r=10){if(!this.tryParseString(e,r))throw new Error(`Failed to parse string as uint64 value: ${JSON.stringify(e)}.`);return this}static parseString(e,r=10){return new M().parseString(e,r)}valid(){const{low:e,high:r}=this;return e>>>0===e&&r>>>0===r}toJSON(){return this.toString()}static lshift(e,r,i){const{low:m,high:_}=r;return i===0?(e.low=m,e.high=_):i<32?(e.low=m<<i,e.high=_<<i|m>>>32-i):(e.low=0,e.high=m<<i-32),e}static rshift(e,r,i){const{low:m,high:_}=r;return i===0?(e.low=m,e.high=_):i<32?(e.low=m>>>i|_<<32-i,e.high=_>>>i):(e.low=_>>>i-32,e.high=0),e}static or(e,r,i){return e.low=r.low|i.low,e.high=r.high|i.high,e}static xor(e,r,i){return e.low=r.low^i.low,e.high=r.high^i.high,e}static and(e,r,i){return e.low=r.low&i.low,e.high=r.high&i.high,e}static add(e,r,i){const m=r.low+i.low;let _=r.high+i.high;const E=m>>>0;return E!==m&&(_+=1),e.low=E,e.high=_>>>0,e}static addUint32(e,r,i){const m=r.low+i;let _=r.high;const E=m>>>0;return E!==m&&(_+=1),e.low=E,e.high=_>>>0,e}static decrement(e,r){let{low:i,high:m}=r;return i===0&&(m-=1),e.low=i-1>>>0,e.high=m>>>0,e}static increment(e,r){let{low:i,high:m}=r;return i===4294967295&&(m+=1),e.low=i+1>>>0,e.high=m>>>0,e}static subtract(e,r,i){const m=r.low-i.low;let _=r.high-i.high;const E=m>>>0;return E!==m&&(_-=1),e.low=E,e.high=_>>>0,e}static absDifference(e,r,i){return M.less(r,i)?M.subtract(e,i,r):M.subtract(e,r,i)}static multiplyUint32(e,r,i){const{low:m,high:_}=r;return e.low=Math.imul(m,i)>>>0,e.high=Math.imul(_,i)+u(m,i)>>>0,e}static lowMask(e,r){return r===0?e.high=e.low=0:r<=32?(e.high=0,e.low=4294967295>>>32-r):(e.high=4294967295>>>r-32,e.low=4294967295),e}toNumber(){return this.low+this.high*4294967296}setFromNumber(e){e=Math.round(e),e<0?this.low=this.high=0:e>=18446744073709552e3?this.low=this.high=4294967295:(this.low=e%4294967296,this.high=Math.floor(e/4294967296))}static fromNumber(e){const r=new M;return r.setFromNumber(e),r}};o.ZERO=new o(0,0),o.ONE=new o(1,0);let n=o},310:(R,h,l)=>{l.d(h,{y:()=>t});var a=l(4704);/**
 * @license
 * Copyright 2016 Google Inc.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const s=!1;function t(u){const o={antialias:!1,stencil:!0};s&&(console.log("DEBUGGING via preserveDrawingBuffer"),o.preserveDrawingBuffer=!0);const n=u.getContext("webgl2",o);if(n==null)throw new Error("WebGL not supported.");n.memoize=new a.d,n.maxTextureSize=n.getParameter(n.MAX_TEXTURE_SIZE),n.max3dTextureSize=n.getParameter(n.MAX_3D_TEXTURE_SIZE),n.maxTextureImageUnits=n.getParameter(n.MAX_TEXTURE_IMAGE_UNITS),n.tempTextureUnit=n.maxTextureImageUnits-1;for(const f of["EXT_color_buffer_float"])if(!n.getExtension(f))throw new Error(`${f} extension not available`);for(const f of["EXT_float_blend"])n.getExtension(f);return n}}};export{A as id,T as ids,C as modules};

//# sourceMappingURL=549.fdd457b9762ae40f7aa3.js.map