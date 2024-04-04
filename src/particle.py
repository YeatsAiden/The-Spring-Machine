import pygame
from core_funcs import *
from settings import *


class Particle:
    def __init__(self):
        self.proccesses = {}
        
        
    def change_color(self, image, color):
        color_img = pygame.Surface(image.get_size())
        color_img.fill(color)
        
        image = image.copy()
        image.blit(color_img, (0, 0), special_flags = pygame.BLEND_MULT)
        return image
    
    # "dirt_explosion", 2, True, False, dirt_img, 0.1
    def create_proccess(self, name, duration, make_collisions, infinite, gravity, limit, amount):
        # Please if you are reviewing this code. i know it's terrible. it's from like a year ago. Was to lazy to make a new particle system....:[
        self.proccesses.update({
            name:{
                "duration": duration * 60,
                "can_append": True,
                "repetition_index": 0,
                "particles": [],
                "limit": limit,
                "make_collisions": make_collisions,
                "infinite": infinite,
                "gravity": gravity,
                "time_since": 0,
                "amount": amount,
                }
            })


    # particle array structure => [pos, vel, size, size_change, duration, rect, image]
    def particle_process(self, surf, new_particle, particle_proccess_name, scroll, tiles, current_time, dt):
        if (self.proccesses[particle_proccess_name]["can_append"] or self.proccesses[particle_proccess_name]["infinite"]) and len(self.proccesses[particle_proccess_name]["particles"]) < self.proccesses[particle_proccess_name]["limit"] and timer(current_time, self.proccesses[particle_proccess_name]["time_since"], self.proccesses[particle_proccess_name]["amount"]):
            self.proccesses[particle_proccess_name]["time_since"] = time.time()
            self.proccesses[particle_proccess_name]["particles"].append(new_particle)

        if self.proccesses[particle_proccess_name]["repetition_index"] >= self.proccesses[particle_proccess_name]["duration"]:
            self.proccesses[particle_proccess_name]["can_append"] = False
            self.proccesses[particle_proccess_name]["repetition_index"] = 0

        if len(self.proccesses[particle_proccess_name]["particles"]) > 0:
            for particle in self.proccesses[particle_proccess_name]["particles"]:
                if not self.proccesses[particle_proccess_name]["make_collisions"]:
                    particle[0][0] += particle[1][0] * dt
                    particle[0][1] += particle[1][1] * dt
                else:
                    particle[0][0] += particle[1][0] * dt
                    particle[5].centerx = particle[0][0]
                    for layer in tiles:
                        for tile in tiles[layer]:
                            if tiles[layer][tile].colliderect(particle[5]):
                                particle[1][0] *= -0.5 * dt
                                particle[0][0] += particle[1][0] * 2
                    particle[0][1] += particle[1][1] * dt
                    particle[5].centery = particle[0][1]
                    for layer in tiles:
                        for tile in tiles[layer]:
                            if tiles[layer][tile].colliderect(particle[5]):
                                particle[1][1] *= -0.5 * dt
                                particle[0][1] += particle[1][1] * 2

                img = pygame.transform.scale(particle[6], [particle[2], particle[2]])
                surf.blit(img, (particle[0][0] - scroll[0], particle[0][1] - scroll[1]))

                particle[4] -= dt
                particle[1][1] += self.proccesses[particle_proccess_name]["gravity"]
                particle[2] += particle[3]

                if particle[2] < 0:
                    particle[2] = 0

                if particle[4] <= 0:
                    self.proccesses[particle_proccess_name]["particles"].remove(particle)

        self.proccesses[particle_proccess_name]["repetition_index"] += 1

            