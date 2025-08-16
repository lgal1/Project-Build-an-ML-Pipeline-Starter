import wandb
import pandas as pd

# Start a W&B run
run = wandb.init(project="Project-Build-an-ML-Pipeline-Starter", job_type="basic_cleaning") 

# Create the artifact
artifact = wandb.Artifact(
    name=args.output_artifact, 
    type=args.output_type, 
    description=args.output_description
)

# Add the cleaned file
artifact.add_file("clean_sample.csv")

# Log the artifact to the run
run.log_artifact(artifact)

# Optional: finish the run
run.finish()
