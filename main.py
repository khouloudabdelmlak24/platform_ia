from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok"}


# Les noms des champs sont identiques à ceux du backend Spring Boot
# (MeasurementRequest), pour pouvoir lui transmettre les données sans conversion.
class PredictRequest(BaseModel):
    systolicPressure: int
    diastolicPressure: int
    bloodGlucose: Optional[float] = None
    cholesterol: Optional[float] = None
    weight: Optional[float] = None
    height: Optional[float] = None  # en centimètres


class PredictResponse(BaseModel):
    riskLevel: str
    riskScore: int
    factors: List[str]
    model: str


@app.post("/predict", response_model=PredictResponse)
def predict(data: PredictRequest):
    """
    RÉPONSE SIMULÉE (mock) : ce n'est pas un vrai modèle médical.
    Elle applique des règles simples pour fournir un contrat d'échange stable.
    Le vrai modèle pourra remplacer ce calcul sans changer la forme de la réponse.
    """
    score = 0
    factors: List[str] = []

    # Tension artérielle
    if data.systolicPressure >= 140 or data.diastolicPressure >= 90:
        score += 2
        factors.append("Tension élevée")
    elif data.systolicPressure >= 130 or data.diastolicPressure >= 85:
        score += 1
        factors.append("Tension limite")

    # Glycémie (hypothèse : g/L, comme les valeurs de test déjà en base)
    if data.bloodGlucose is not None:
        if data.bloodGlucose >= 1.26:
            score += 2
            factors.append("Glycémie élevée")
        elif data.bloodGlucose >= 1.10:
            score += 1
            factors.append("Glycémie limite")

    # Cholestérol (hypothèse : g/L)
    if data.cholesterol is not None:
        if data.cholesterol >= 2.4:
            score += 2
            factors.append("Cholestérol élevé")
        elif data.cholesterol >= 2.0:
            score += 1
            factors.append("Cholestérol limite")

    # IMC (BMI) calculé si poids et taille sont fournis
    if data.weight and data.height and data.height > 0:
        height_m = data.height / 100
        bmi = data.weight / (height_m * height_m)
        if bmi >= 30:
            score += 2
            factors.append("Obésité")
        elif bmi >= 25:
            score += 1
            factors.append("Surpoids")

    if score >= 4:
        level = "HIGH"
    elif score >= 2:
        level = "MODERATE"
    else:
        level = "LOW"

    return PredictResponse(
        riskLevel=level,
        riskScore=score,
        factors=factors,
        model="mock-v1",
    )