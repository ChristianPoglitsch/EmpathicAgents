import sys
sys.path.append('../../')
from LLM_Character.world.validation_dataclass import * 

# Example data
example_setup_data = SetupData(
    meta=MetaData(
        fork_sim_code="FS123",
        sim_code="SIM456",
        curr_time="2024-08-13T12:00:00Z",
        sec_per_step=60,
        persona_names=["Alice", "Bob"],
        step=1
    ),
    personas={
        "Alice": PersonaData(
            scratch_data=PersonaScratchData(
                curr_time="2024-08-13T12:00:00Z",
                daily_plan_req="Complete project report",
                name="Alice Smith",
                first_name="Alice",
                last_name="Smith",
                age=30,
                innate="Creative",
                learned="Data Analysis",
                currently="Working on project X",
                lifestyle="Active",
                living_area=OneLocationData(
                    world="WorldA",
                    sectors=[Sector(
                        sector="Sector1",
                        arenas=[Arena(
                            arena="Arena1",
                            gameobjects=[GameObject(gameobject="Object1")]
                        )]
                    )]
                ),
                recency_w=5,
                relevance_w=3,
                importance_w=7,
                recency_decay=2,
                importance_trigger_max=10,
                importance_trigger_curr=4,
                importance_ele_n=8,
                daily_req=["Complete report", "Attend meeting"],
                f_daily_schedule=["09:00 AM - Work", "12:00 PM - Lunch", "03:00 PM - Meeting"],
                f_daily_schedule_hourly_org=["09:00 AM - Start", "12:00 PM - Lunch", "03:00 PM - Meeting"],
                act_address=OneLocationData(
                    world="WorldA",
                    sectors=[Sector(
                        sector="Sector1",
                        arenas=[Arena(
                            arena="Arena1",
                            gameobjects=[GameObject(gameobject="Object2")]
                        )]
                    )]
                ),
                act_start_time="2024-08-13T14:00:00Z",
                act_duration="2h",
                act_description="Work on the project X",
                act_event=("Meeting", "Zoom", "2024-08-13T15:00:00Z"),
                chatting_with="Bob",
                chat=[["Hi Bob", "Hello Alice"], ["How's the project going?", "Pretty well"]],
                chatting_with_buffer={"Bob": "Waiting for your update"},
                chatting_end_time="2024-08-13T15:30:00Z"
            ),
            spatial_data=LocationData(
                world="WorldA",
                sectors=[Sector(
                    sector="Sector1",
                    arenas=[Arena(
                        arena="Arena1",
                        gameobjects=[GameObject(gameobject="Object1")]
                    )]
                )]
            ),
            as_mem_data=AssociativeMemoryData(
                embeddings={"event_1": [0.1, 0.2, 0.3]},
                kw_strenght=KwStrengthData(
                    kw_strength_event={"event_1": 5},
                    kw_strength_thought={"thought_1": 7}
                ),
                nodes={
                    "node_1": Node(
                        node_id=1,
                        node_count=1,
                        type_count=1,
                        type="Event",
                        depth=1,
                        created="2024-08-01T10:00:00Z",
                        expiration=None,
                        subject="Project X",
                        predicate="Has",
                        object="Deadline",
                        description="Project X has a deadline",
                        embedding_key="event_1",
                        poignancy=8,
                        keywords=["Project", "Deadline"],
                        filling=["Details about the deadline"]
                    )
                }
            )
        ),
        "Bob": PersonaData(
            scratch_data=PersonaScratchData(
                curr_time="2024-08-13T12:00:00Z",
                daily_plan_req="Prepare presentation",
                name="Bob Johnson",
                first_name="Bob",
                last_name="Johnson",
                age=28,
                innate="Analytical",
                learned="Project Management",
                currently="Preparing for presentation",
                lifestyle="Balanced",
                living_area=OneLocationData(
                    world="WorldA",
                    sectors=[Sector(
                        sector="Sector2",
                        arenas=[Arena(
                            arena="Arena2",
                            gameobjects=[GameObject(gameobject="Object3")]
                        )]
                    )]
                ),
                recency_w=4,
                relevance_w=6,
                importance_w=5,
                recency_decay=3,
                importance_trigger_max=8,
                importance_trigger_curr=3,
                importance_ele_n=5,
                daily_req=["Prepare slides", "Rehearse presentation"],
                f_daily_schedule=["10:00 AM - Work", "01:00 PM - Lunch", "04:00 PM - Presentation rehearsal"],
                f_daily_schedule_hourly_org=["10:00 AM - Start", "01:00 PM - Lunch", "04:00 PM - Rehearse"],
                act_address=OneLocationData(
                    world="WorldA",
                    sectors=[Sector(
                        sector="Sector2",
                        arenas=[Arena(
                            arena="Arena2",
                            gameobjects=[GameObject(gameobject="Object4")]
                        )]
                    )]
                ),
                act_start_time="2024-08-13T16:00:00Z",
                act_duration="1h",
                act_description="Rehearse presentation for the upcoming meeting",
                act_event=("Rehearsal", "Google Meet", "2024-08-13T17:00:00Z"),
                chatting_with="Alice",
                chat=[["Hi Alice", "Hey Bob"], ["How's the presentation?", "Almost ready"]],
                chatting_with_buffer={"Alice": "Let me know if you need help"},
                chatting_end_time="2024-08-13T17:30:00Z"
            ),
            spatial_data=LocationData(
                world="WorldA",
                sectors=[Sector(
                    sector="Sector2",
                    arenas=[Arena(
                        arena="Arena2",
                        gameobjects=[GameObject(gameobject="Object3")]
                    )]
                )]
            ),
            as_mem_data=AssociativeMemoryData(
                embeddings={"event_2": [0.4, 0.5, 0.6]},
                kw_strenght=KwStrengthData(
                    kw_strength_event={"event_2": 6},
                    kw_strength_thought={"thought_2": 8}
                ),
                nodes={
                    "node_2": Node(
                        node_id=2,
                        node_count=2,
                        type_count=1,
                        type="Task",
                        depth=1,
                        created="2024-08-01T11:00:00Z",
                        expiration=None,
                        subject="Presentation",
                        predicate="Requires",
                        object="Rehearsal",
                        description="The presentation requires rehearsal",
                        embedding_key="event_2",
                        poignancy=7,
                        keywords=["Presentation", "Rehearsal"],
                        filling=["Details about the presentation rehearsal"]
                    )
                }
            )
        )
    },
    virtual_world=LocationData(
        world="WorldA",
        sectors=[
            Sector(
                sector="Sector1",
                arenas=[Arena(
                    arena="Arena1",
                    gameobjects=[GameObject(gameobject="Object1")]
                )]
            ),
            Sector(
                sector="Sector2",
                arenas=[Arena(
                    arena="Arena2",
                    gameobjects=[GameObject(gameobject="Object2")]
                )]
            )
        ]
    )
)

example_update_message = UpdateMessage(
    type="update",
    data=[
        OneLocationData(
            character_name=["Alice"],
            current_location=OneLocationData(
                world="WorldA",
                sectors=[
                    Sector(
                        sector="Sector1",
                        arenas=[Arena(
                            arena="Arena1",
                            gameobjects=[GameObject(gameobject="Object1")]
                        )]
                    )
                ]
            )
        ),
        OneLocationData(
            character_name=["Bob"],
            current_location=OneLocationData(
                world="WorldA",
                sectors=[
                    Sector(
                        sector="Sector2",
                        arenas=[Arena(
                            arena="Arena2",
                            gameobjects=[GameObject(gameobject="Object3")]
                        )]
                    )
                ]
            )
        )
    ]
)

if __name__ == "__main__":
    print(example_setup_data)
    print(example_update_message)