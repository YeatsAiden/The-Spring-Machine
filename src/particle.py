import pygame
from core_funcs import *


class Particle:
    def __init__(self):
        self.proccesses = {}
        
        
    def chang_color(self, image, color):
        color_img = pygame.Surface(image.get_size())
        color_img.fill(color)
        
        image = image.copy()
        image.blit(color_img, (0, 0), special_flags = pygame.BLEND_MULT)
        return image
    
    # "dirt_explosion", 2, True, False, dirt_img, 0.1
    def create_proccess(self, name, duration, make_collisions, infinite, gravity, limit):
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
                }
            })


    # particle array structure => [pos, vel, size, size_change, duration, count_down, rect, image]

    def particle_process(self, surf, new_particle, particle_proccess_name, scroll, tiles, current_time):
        if (self.proccesses[particle_proccess_name]["can_append"] or self.proccesses[particle_proccess_name]["infinite"]) and len(self.proccesses[particle_proccess_name]["particles"]) < self.proccesses[particle_proccess_name]["limit"] and timer(current_time, ):
            self.proccesses[particle_proccess_name]["time_since"]
            self.proccesses[particle_proccess_name]["particles"].append(new_particle)

        if self.proccesses[particle_proccess_name]["repetition_index"] >= self.proccesses[particle_proccess_name]["duration"]:
            self.proccesses[particle_proccess_name]["can_append"] = False
            self.proccesses[particle_proccess_name]["repetition_index"] = 0

        if len(self.proccesses[particle_proccess_name]["particles"]) > 0:
            for particle in self.proccesses[particle_proccess_name]["particles"]:
                if not self.proccesses[particle_proccess_name]["make_collisions"]:
                    particle[0][0] += particle[1][0]
                    particle[0][1] += particle[1][1]
                    particle[1][1] += self.proccesses[particle_proccess_name]["gravity"]
                else:
                    particle[1][1] += self.proccesses[particle_proccess_name]["gravity"]
                    particle[0][0] += particle[1][0]
                    particle[6].x = particle[0][0]
                    for layer in tiles:
                        for tile in tiles[layer]:
                            if tiles[layer][tile].colliderect(particle[6]):
                                particle[1][0] *= -0.5
                                particle[0][0] += particle[1][0] * 2
                    particle[0][1] += particle[1][1]
                    particle[6].y = particle[0][1]
                    for layer in tiles:
                        for tile in tiles[layer]:
                            if tiles[layer][tile].colliderect(particle[6]):
                                particle[1][1] *= -0.5
                                particle[0][1] += particle[1][1] * 2

                img = pygame.transform.scale(particle[7], [particle[2], particle[2]])
                surf.blit(img, (particle[0][0] - scroll[0], particle[0][1] - scroll[1]))

                particle[4] -= particle[5]
                particle[2] += particle[3]

                if particle[2] < 0:
                    particle[2] = 0

                if particle[4] <= 0:
                    self.proccesses[particle_proccess_name]["particles"].remove(particle)

        self.proccesses[particle_proccess_name]["repetition_index"] += 1

            