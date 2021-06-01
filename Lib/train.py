from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from torchvision import datasets
from torch.utils.data import DataLoader
from PIL import Image
import os

def detectFace(img, path = True):
    '''
    Hàm phát hiện khuôn mặt từ img và trả về 1 torch.Size([3, 240, 240])

    Param: nếu path == True thì img là Relavetive path của ảnh (dùng để train), ngược lại thì img là ảnh dùng để chấm công
    Return: torch.Size([3, 240, 240])
    '''
    detector = MTCNN(image_size=240, margin=0, min_face_size=20) 
    face, prob = detector(img, return_prob = True)
    # plt.imshow(face.permute(1,2,0))
    return face, prob
    
# Các hàm hỗ trợ load ảnh và lưu data
def getIDList(path):
    '''
    Input: path Images folder
    Output: ID list

    Hàm trả về list các ID của User
    '''
    return os.listdir(path)


def collate_fn(x):
    return x[0]

def extractingFolder():
    dataset = datasets.ImageFolder('Indian-celebrities')
    index_to_class = os.listdir("Indian-celebrities")
    loader = DataLoader(dataset, collate_fn=collate_fn)
    
    #khởi tạo MTCNN để phát hiện khuôn mặt
    mtcnn = MTCNN(image_size=240, margin=0, min_face_size=20)
    #khởi tạo resnet để nhúng khuôn mặt thành vector
    resnet = InceptionResnetV1(pretrained='vggface2').eval()

    name_list = [] #danh sách tên của những khuôn mặt
    embedding_list = [] #danh sách các ma trận khuôn mặt đã được nhúng ở bước Resnet

    for img, idx in loader:
        face, prob = mtcnn(img, return_prob=True)
        #nếu khuôn mặt được xác định 
        #và đánh giá tỉ lệ % độ chính xác mà module detect được
        if face is not None and prob>0.95:
            #chuyển khuôn mặt đã được cắt sang resnet model để nhúng thành vector
            emb = resnet(face.unsqueeze(0))
            #chèn kết quả vào danh sách embedding_list
            embedding_list.append(emb.detach())
            #tên của người đó cũng được thêm vào danh sách 
            name_list.append(index_to_class[idx])

    data = [embedding_list, name_list]
    torch.save(data, "data.pt")

def face_match(img_path, data_path):
    #gọi hàm xác định khuôn mặt
    img = Image.open(img_path)
    face, prob = detectFace(img)
    resnet = InceptionResnetV1(pretrained='vggface2').eval()
    if face is not None and prob>0.90:
    #trả về một ảnh cắt khuôn mặt và tỉ lệ % độ chính xác
        emb = resnet(face.unsqueeze(0)).detach()
        #gradient false
        saved_data = torch.load('data.pt')
        embedding_list = saved_data[0]
        name_list = saved_data[1]
        dist_list = [] #danh sách khoảng cách của test và vector train

    for idx, emb_db in enumerate(embedding_list):
        #tính khoảng cách giữa emb test với emb database trong file pt
        dist = torch.dist(emb, emb_db).item()
        dist_list.append(dist)
    idx_min = dist_list.index(min(dist_list))
    return (name_list[idx_min], min(dist_list)) if min(dist_list) <= 0.9 else -1


extractingFolder()
result = face_match("download.jpg", "data.pt")

if result != -1:
    print('Face matched with: ', result[0], 'with distance: ', result[1])
else:
    print("No exist")