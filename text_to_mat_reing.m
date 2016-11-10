


function []=text_to_mat_reing()
    %convert txt files to mat files
    clear

    samprate=30;
    FiltHz=11;
    %basepath='/media/claudio/INTENSO/Social-behaviour/isr_social_behaviour_dataset_images'
    basepath='/media/ccoppola/52FFC5D351F60A1C/Social-Activities-Data_images';
    %basepath='~/LCAS/isr_social_behaviour_dataset/';
    Rec_Folders=dir(basepath);Rec_Folders(1:2)=[];
    %Sessions(10,2)=struct('action',cell(8,1));
    Sessions(length(Rec_Folders),2).action=cell(8,1);
    Sessions_filt(length(Rec_Folders),2).action=cell(8,1);

    for bag=1:length(Rec_Folders)    


        folder=strcat('/',Rec_Folders(bag).name,'/');
        txtfiles=dir([basepath,folder,'*user*.txt']);
        
        filename1=txtfiles(~cellfun(@isempty,strfind({txtfiles.name},'_user1'))).name;
        filename2=txtfiles( cellfun(@isempty,strfind({txtfiles.name},'_user1'))).name;
        
        F1=fopen(strcat(basepath,folder,filename1));
        F2=fopen(strcat(basepath,folder,filename2));

        if F1<0 || F2<0
            %system(strcat(['cat ',basepath],folder,'a',num2str(act,'%02d'),'_s',num2str(session,'%02d'),'*_camera_usr',num2str(user,'%d'),'.txt >> temp.txt'));
            %F1=fopen(strcat('temp.txt'));
            error('file not openable')
            %system('rm temp.txt');
            %fclose(F1);
        else
            disp([filename1,' ',filename2])
            temp1=cell2mat(textscan(F1, repmat('%f ',1,90), 'delimiter', '\n', 'whitespace', ''));
            temp2=cell2mat(textscan(F2, repmat('%f ',1,90), 'delimiter', '\n', 'whitespace', ''));
            minrows=min(size(temp1,1),size(temp2,1));
            Sessions(bag,1).action=temp1(1:minrows,:);
            Sessions(bag,2).action=temp2(1:minrows,:);
            fclose(F1);
            fclose(F2);
        end

    end


%     for session=1:10
% 
%         for  act=1:8
% 
%             for user=1:2
%                 Sessions_filt(session,user).action{act}=filter(FiltHz/samprate, [1 FiltHz/samprate-1], Sessions(1,1).action{1});
%             end
% 
%         end
% 
% 
%     end



    save([basepath,'/dataset.mat'],'Sessions','-v7.3');
%     save([basepath,'/dataset_filt.mat'],'Sessions_filt','-v7.3');
end



