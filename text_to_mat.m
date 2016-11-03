%convert txt files to mat files
clear

samprate=30;
FiltHz=11;
%basepath='/media/claudio/INTENSO/Social-behaviour/isr_social_behaviour_dataset_images'
basepath='~/LCAS/Social-behaviour/isr_social_behaviour_dataset_images/';
%basepath='~/LCAS/isr_social_behaviour_dataset/';

%Sessions(10,2)=struct('action',cell(8,1));
Sessions(10,2).action=cell(8,1);
Sessions_filt(10,2).action=cell(8,1);
for i=1:19 
    Sessions(i).action=cell(8,1);
    Sessions_filt(i).action=cell(8,1);
end
for session=1:10

    for  act=1:8
        
            folder=strcat('/session_',num2str(session,'%02d'),'/act_',num2str(act,'%02d'),'/');
            %folder=strcat('act_',num2str(act,'%02d'),'/session_',num2str(session,'%02d'),'/');
            %filename1=strcat('a',num2str(act,'%02d'),'_s',num2str(session,'%02d'),'_camera_usr',num2str(1,'%d'),'.txt');
            %filename2=strcat('a',num2str(act,'%02d'),'_s',num2str(session,'%02d'),'_camera_usr',num2str(2,'%d'),'.txt');
            filename1=strcat('a',num2str(act,'%02d'),'_s',num2str(session,'%02d'),'_user',num2str(1,'%d'),'.txt');
            filename2=strcat('a',num2str(act,'%02d'),'_s',num2str(session,'%02d'),'_user',num2str(2,'%d'),'.txt');
            F1=fopen(strcat(basepath,folder,filename1));
            F2=fopen(strcat(basepath,folder,filename2));
            
            if F1<0 || F2<0
                %system(strcat(['cat ',basepath],folder,'a',num2str(act,'%02d'),'_s',num2str(session,'%02d'),'*_camera_usr',num2str(user,'%d'),'.txt >> temp.txt'));
                %F1=fopen(strcat('temp.txt'));
                filelist1=strsplit(ls(strcat(basepath,folder,'*_user1.txt')))';
                filelist2=strsplit(ls(strcat(basepath,folder,'*_user2.txt')))';
                
                
                [~,namelist1,c]=fileparts(filelist1{1});
                [~,namelist2,c]=fileparts(filelist2{1});
                
                disp('-------------------------------------------')
                disp([[namelist1,c],' ',[namelist2,c]])
                disp('-------------------------------------------')
                for f=1:(size(filelist1,1)-1)
                    F1=fopen(filelist1{f});
                    F2=fopen(filelist2{f});
                    temp1=cell2mat(textscan(F1, repmat('%f ',1,90), 'delimiter', '\n', 'whitespace', ''));
                    temp2=cell2mat(textscan(F2, repmat('%f ',1,90), 'delimiter', '\n', 'whitespace', ''));
                    minrows=min(size(temp1,1),size(temp2,1));
                    Sessions(session,1).action{act}=[Sessions(session,1).action{act};temp1(1:minrows,:)];
                    Sessions(session,2).action{act}=[Sessions(session,2).action{act};temp2(1:minrows,:)];
                    fclose(F1);
                    fclose(F2);
                end
                %system('rm temp.txt');
                %fclose(F1);
            else
                disp([filename1,' ',filename2])
                temp1=cell2mat(textscan(F1, repmat('%f ',1,90), 'delimiter', '\n', 'whitespace', ''));
                temp2=cell2mat(textscan(F2, repmat('%f ',1,90), 'delimiter', '\n', 'whitespace', ''));
                minrows=min(size(temp1,1),size(temp2,1));
                Sessions(session,1).action{act}=temp1(1:minrows,:);
                Sessions(session,2).action{act}=temp2(1:minrows,:);
                fclose(F1);
                fclose(F2);
            end
            
        
        
    end
    
    
end


for session=1:10

    for  act=1:8
        
        for user=1:2
            Sessions_filt(session,user).action{act}=filter(FiltHz/samprate, [1 FiltHz/samprate-1], Sessions(1,1).action{1});
        end
        
    end
    
    
end



save([basepath,'/dataset.mat'],'Sessions','-v7.3');
save([basepath,'/dataset_filt.mat'],'Sessions_filt','-v7.3');
