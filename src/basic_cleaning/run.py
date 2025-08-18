#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import pandas as pd
import wandb

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger(__name__)

# DO NOT MODIFY
def go(args):

    run = wandb.init(project="nyc_airbnb", job_type="basic_cleaning",
                     group="cleaning", save_code=True)
    run.config.update(vars(args))

    # Download input artifact. This will also log that this script is using this
    logger.info("Downloading input artifact: %s", args.input_artifact)
    artifact_local_path = run.use_artifact(args.input_artifact).file()

    df = pd.read_csv(artifact_local_path)
    # Drop outliers
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()
    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'], errors="coerce")

    idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()
    # Save the cleaned file
    out_file = "clean_sample.csv" 
    df.to_csv(out_file, index=False)

    

    # log the new data.
    artifact = wandb.Artifact(
     args.output_artifact,
     type=args.output_type,
     description=args.output_description
 )
    artifact.add_file(out_file)
    run.log_artifact(artifact)
    run.finish()


# TODO: In the code below, fill in the data type for each argumemt. The data type should be str, float or int. 
# TODO: In the code below, fill in a description for each argument. The description should be a string.
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")
  
    parser.add_argument(
        "--input_artifact", 
        type = str,
        help="Input W&B artifact to download input artifact",
        required=True,
    )

    parser.add_argument(
        "--output_artifact", 
        type = str,
        help="Name for the output artifact ",
        required=True,
    )

    parser.add_argument(
        "--output_type", 
        type = str,
        help="Artifact type for the output type", 
        required=True,
    )

    parser.add_argument(
        "--output_description", 
        type = str,
        help="Output description of the cleaned artifact ",
        required=True,
    )

    parser.add_argument(
        "--min_price", 
        type = float,
        help="Min nightly price - 10)",
        required=True,
    )

    parser.add_argument(
        "--max_price",
        type = float,
        help="Max nightly price to keep - 350)",
        required=True,
    )


    args = parser.parse_args()

    go(args)