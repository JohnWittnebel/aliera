# This is owned by Player
class LeaderEffectManager():
    def __init__(self):
        self.onPlayEffects = []
        self.turnStartEffects = []
        self.turnEndEffects = []
        self.onSelfDamageEffects = []
        self.onSelfHealEffects = []
        
    def activateOnPlayEffects(self, gameState, card):
        for effect in self.onPlayEffects:
            effect(gameState, card)
