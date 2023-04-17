# This is owned by Player
class LeaderEffectManager():
    def __init__(self):
        self.onPlayEffects = []
        self.turnStartEffects = []
        self.turnEndEffects = []
        self.onSelfHealEffects = []
        self.onSelfPingEffects = []
        self.onCombatDamageEffects = []
        self.onEffectDamageEffects = []
        
    def activateOnPlayEffects(self, gameState, card):
        for effect in self.onPlayEffects:
            effect(gameState, card)
    
    def activateSelfPingEffects(self, gameState):
        for effect in self.onSelfPingEffects:
            effect(gameState)
    
    def activateCombatDamageEffects(self, gameState):
        for effect in self.onCombatDamageEffects:
            effect(gameState)
    
    def activateEffectDamageEffects(self, gameState):
        for effect in self.onEffectDamageEffects:
            effect(gameState)

    def activateHealEffects(self, gameState):
        for effect in self.onSelfHealEffects:
            effect(gameState)
