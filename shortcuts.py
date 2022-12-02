import pygame

def scale_rect(rect, scale, divide=False): # Return a scaled rect
	new_rect = pygame.Rect(rect) # Create new Rect object to avoid changing the original rect

	if divide:
		new_rect.x /= scale
		new_rect.y /= scale
		new_rect.width /= scale
		new_rect.height /= scale

	else:
		new_rect.x *= scale
		new_rect.y *= scale
		new_rect.width *= scale
		new_rect.height *= scale

	return new_rect

def center(p, image): # Center the position to the center of the image by ofsetting the position by have the image dimentions
	return (p[0] - image.get_width() / 2, p[1] - image.get_height() / 2)

def center_bottom(p, image):
	return (p[0] - image.get_width() / 2, p[1] - image.get_height())