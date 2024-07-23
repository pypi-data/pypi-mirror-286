import torch
import torchattacks
import matplotlib.pyplot as plt
import numpy as np

def def_attack_eval(attack_method, model, test_loader, device, eps=None, num_batches=10):
    successful_attacks = 0
    total_samples = 0
    examples = []
    attack_name = attack_method.__name__

    torch.set_grad_enabled(True)

    for batch_idx, (images, labels) in enumerate(test_loader):
        if batch_idx >= num_batches:
            break

        images, labels = images.to(device), labels.to(device)
        images.requires_grad = True

        if eps:
            attack = attack_method(model, eps=eps)
        else:
            attack = attack_method(model)

        adv_images = attack(images, labels)
        original_predictions = model(images)
        adversarial_predictions = model(adv_images)

        original_pred_labels = torch.argmax(original_predictions, dim=1)
        adversarial_pred_labels = torch.argmax(adversarial_predictions, dim=1)

        for i in range(len(labels)):
            if original_pred_labels[i] == labels[i] and original_pred_labels[i] != adversarial_pred_labels[i]:
                successful_attacks += 1
                examples.append((images[i].cpu(), adv_images[i].cpu(), labels[i].cpu(), original_pred_labels[i].cpu(), adversarial_pred_labels[i].cpu()))

        total_samples += labels.size(0)

    torch.set_grad_enabled(False)

    success_rate = successful_attacks / total_samples
    print(f'Success Rate of {attack_name}: {success_rate}')

    visualize_examples(examples, test_loader.dataset.classes)

def attack_eval(attack_method, model, test_loader, device, num_batches=10, **kwargs):
    successful_attacks = 0
    total_samples = 0
    examples = []

    torch.set_grad_enabled(True)

    for batch_idx, (images, labels) in enumerate(test_loader):
        if batch_idx >= num_batches:
            break

        images, labels = images.to(device), labels.to(device)
        images.requires_grad = True

        attack = attack_method(model, **kwargs)
        adv_images = attack(images, labels)
        original_predictions = model(images)
        adversarial_predictions = model(adv_images)

        original_pred_labels = torch.argmax(original_predictions, dim=1)
        adversarial_pred_labels = torch.argmax(adversarial_predictions, dim=1)

        for i in range(len(labels)):
            if original_pred_labels[i] == labels[i] and original_pred_labels[i] != adversarial_pred_labels[i]:
                successful_attacks += 1
                examples.append((images[i].cpu(), adv_images[i].cpu(), labels[i].cpu(), original_pred_labels[i].cpu(), adversarial_pred_labels[i].cpu()))

        total_samples += labels.size(0)

    torch.set_grad_enabled(False)

    success_rate = successful_attacks / total_samples
    attack_name = attack_method.__name__
    print(f'Success Rate of {attack_name} attack: {success_rate}')

    visualize_examples(examples, test_loader.dataset.classes)


def visualize_examples(examples, class_names):
    if len(examples) > 0:
        num_examples_to_show = min(5, len(examples))
        fig, axs = plt.subplots(num_examples_to_show, 2, figsize=(10, 5 * num_examples_to_show))
        for i in range(num_examples_to_show):
            original_image, adv_image, true_label, orig_pred, adv_pred = examples[i]

            axs[i, 0].imshow(np.transpose(original_image / 2 + 0.5, (1, 2, 0)))
            axs[i, 0].set_title(f"Original Image\nTrue: {class_names[true_label]}\nPred: {class_names[orig_pred]}")
            axs[i, 0].axis('off')

            axs[i, 1].imshow(np.transpose(adv_image / 2 + 0.5, (1, 2, 0)))
            axs[i, 1].set_title(f"Adversarial Image\nTrue: {class_names[true_label]}\nAdv Pred: {class_names[adv_pred]}")
            axs[i, 1].axis('off')

        plt.tight_layout()
        plt.show()
    else:
        print("No successful adversarial attacks were found.")