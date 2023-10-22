import torch
import clip
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def cv_cls_openai(img, texts):
    image = preprocess(img).unsqueeze(0).to(device)
    text = clip.tokenize(texts).to(device)

    with torch.no_grad():
        # image_features = model.encode_image(image)
        # text_features = model.encode_text(text)
        
        logits_per_image, logits_per_text = model(image, text)
        probs = logits_per_image.softmax(dim=-1).cpu().numpy()

    # print("Label probs:", probs)  # prints: [[0.9927937  0.00421068 0.00299572]]
    return texts[probs.argmax()]

if __name__ == '__main__':
    result = cv_cls_openai(Image.open("CLIP.png"), ["a diagram", "a dog", "a cat"])
    print('result:', result)
