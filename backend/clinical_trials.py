import requests
import json

CLINICAL_TRIALS_URL = "https://clinicaltrials.gov/api/v2/studies"


def search_trials(query, limit=10):
    params = {
        "query.term": query,
        "pageSize": limit,
        "format": "json",
    }

    response = requests.get(
        CLINICAL_TRIALS_URL,
        params=params,
        timeout=20,
    )

    response.raise_for_status()

    data = response.json()

    trials = []

    for study in data.get("studies", []):
        protocol = study.get("protocolSection", {})

        identification = protocol.get(
            "identificationModule", {}
        )

        status_module = protocol.get(
            "statusModule", {}
        )

        conditions_module = protocol.get(
            "conditionsModule", {}
        )

        description_module = protocol.get(
            "descriptionModule", {}
        )

        design_module = protocol.get(
            "designModule", {}
        )

        contacts_module = protocol.get(
            "contactsLocationsModule", {}
        )

        nct_id = identification.get("nctId")

        trial = {
            "nct_id": nct_id,

            "title": identification.get(
                "briefTitle",
                "Untitled study"
            ),

            "official_title": identification.get(
                "officialTitle"
            ),

            "status": status_module.get(
                "overallStatus"
            ),

            "conditions": conditions_module.get(
                "conditions",
                []
            ),

            "brief_summary": description_module.get(
                "briefSummary",
                ""
            ),

            "study_type": design_module.get(
                "studyType"
            ),

            "locations": contacts_module.get(
                "locations",
                []
            ),

            "url": (
                f"https://clinicaltrials.gov/study/{nct_id}"
                if nct_id
                else None
            ),
        }

        trials.append(trial)
        print(f"Retrieved trial: {trial['nct_id']} - {trial['title']}")

    return trials

search_trials("alzheimer", limit=5)