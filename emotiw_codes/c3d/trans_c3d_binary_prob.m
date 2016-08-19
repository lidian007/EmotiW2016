%
%  Licensed under the Creative Commons Attribution-NonCommercial 3.0 
%  License (the "License"). You may obtain a copy of the License at 
%  https://creativecommons.org/licenses/by-nc/3.0/.
%  Unless required by applicable law or agreed to in writing, software 
%  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT 
%  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the 
%  License for the specific language governing permissions and limitations 
%  under the License.
%
% 
function trans_c3d_binary_prob()

fn = './output_probs_afew_1/';
save_dir = './output_probs_afew_1_prob/';
read_binary_blob(fn, save_dir)

fn = './output_probs_afew_2/';
save_dir = './output_probs_afew_2_prob/';
read_binary_blob(fn, save_dir)

fn = './output_probs_qiyi/';
save_dir = './output_probs_qiyi_prob/';
read_binary_blob(fn, save_dir)


function read_binary_blob(fn, save_dir)
vids = clean_dir(fn);
mkdir(save_dir);
for id = 1 : length(vids)
    feats = clean_dir(strcat(fn,vids{id}));
    mkdir(strcat(save_dir, vids{id}));
    for feat_id = 1 : length(feats)
        if strfind(feats{feat_id},'prob')
            feat_name = strcat(fn,vids{id},'/',feats{feat_id});
            [s, data] = read_single_binary_blob(feat_name);
            save_name = strcat(save_dir,vids{id},'/',feats{feat_id});
            fid = fopen(save_name, 'w');
            for i = 1 : length(data)
                fprintf(fid,'%g,',data(i));
            end
            fclose(fid);
        end
    end
end

    


function [s, data] = read_single_binary_blob(fn)
f = fopen(fn, 'r');
s = fread(f, [1 5], 'int32');

% s contains size of the blob e.g. num x chanel x length x height x width
m = s(1)*s(2)*s(3)*s(4)*s(5);

% data is the blob binary data in single precision (e.g float in C++)
data = fread(f, [1 m], 'single');
fclose(f);

function files = clean_dir(base)
  %clean_dir just runs dir and eliminates files in a foldr
  files = dir(base);
  files_tmp = {};
  for i = 1:length(files)
    if strncmpi(files(i).name, '.',1) == 0
      files_tmp{length(files_tmp)+1} = files(i).name;
    end
  end
  files = files_tmp; 



