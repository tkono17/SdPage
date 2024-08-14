import sdmodel as sdm

CT = sdm.CT
CI = sdm.CI

model = CI('A', 'Building')
# A
# A.1F, A.1F.1, A.1F.2
# A.2F, A.2F.1, A.2F.2

components = [
    CT('Building').setChildren([
        CI('1F', 'Floor'), 
        CI('2F', 'Floor'), 
        ]), 
    CT('Floor').setChildren([
        CI('1', 'Room', area=20.0), 
        CI('2', 'Room', area=32.0), 
    ]), 
]

