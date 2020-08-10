# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2020, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

import os
from operator import itemgetter
from pathlib import Path
from shutil import copytree


class SaveFinalCheckPoint(object):
    """
    Experiment mixin to save a copy of the final checkpoint from `logdir` upon
    `stop_experiment`.

    :param config:

        - copy_checkpoint_dir: (optional) name of directory to save a copy of the final
                               checkpoint. The string may contain:
                                    * {name} - name of experiment; taken from config
                                    * {wandb_project} - taken from wandb_args
                                    * {trainable_id} - inferred from logdir

    Example
    ```
    config["name"] = "my_experiment"
    config["logdir"] = ".../ImagenetTrainable_...-45xrhk_mc2"
    config["wandb_args"] = dict(..., project="my_project")
    config["copy_checkpoint_dir"] = "/mnt/.../{wandb_project}/{name}/{trainable_id}/"

    ... 200 epochs of training

    >> checkpoint saved to "/mnt/.../my_project/my_experiment/45xrhk_mc2/checkpoint_200"
    ```
    """

    def setup_experiment(self, config):
        """Setup experiment and get desired path for copied checkpoint."""
        super().setup_experiment(config)

        assert self.logdir
        assert "copy_checkpoint_dir" in config

        self.copy_ckpt_path = config["copy_checkpoint_dir"]

        # Set default formatting.
        self.name = config.get("name", "unknown_name")
        self.wandb_project = "unknown_project"
        self.trainable_id = "unknown_id"

        # Retrieve project name if any - this may or may not be used.
        if "{wandb_project}" in self.copy_ckpt_path:
            wandb_args = config.get("wandb_args", {})
            self.wandb_project = wandb_args.get("project", "unknown_project")

        # Retrieve run_id - this may or may not be used.
        if "{trainable_id}" in self.copy_ckpt_path:
            self.trainable_id = self.logdir.split("-")[-1]  # e.g. 45xrhk_mc2

    def stop_experiment(self):
        """
        Copy over last checkpoint to specified directory.
        """
        super().stop_experiment()
        print("saving final checkpoint", self.rank, type(self.rank), self.rank != 0)
        if self.rank != 0:
            return

        base_path = self.copy_ckpt_path.split("{")[0]
        if not os.path.exists(base_path):
            return

        copy_ckpt_path = self.copy_ckpt_path.replace("{name}", self.name)
        copy_ckpt_path = copy_ckpt_path.replace("{wandb_project}", self.wandb_project)
        copy_ckpt_path = copy_ckpt_path.replace("{trainable_id}", self.trainable_id)
        copy_ckpt_path = Path(copy_ckpt_path)

        # Create the save directory and parents as needed.
        copy_ckpt_path.mkdir(exist_ok=True, parents=True)

        # Find the latest checkpoint.
        log_path = Path(self.logdir)
        checkpoint_paths = []
        for path in log_path.iterdir():
            if "checkpoint" in path.name:
                num = int(path.name.split("_")[1])
                checkpoint_paths.append((num, path))

        checkpoint_paths = sorted(checkpoint_paths, key=itemgetter(0))
        latest_checkpoint = checkpoint_paths[-1][1]  # path of latest

        # Copy over checkpoint.
        try:
            copy_latest_checkpoint = copy_ckpt_path / latest_checkpoint.name
            copytree(src=latest_checkpoint, dst=copy_latest_checkpoint)
            self.logger.info(
                f"Copied over checkpoint from "
                f"{str(latest_checkpoint)} to {str(copy_latest_checkpoint)}."
            )
        except OSError:
            self.logger.warning(
                f"Unable to copy checkpoint from "
                f"{str(latest_checkpoint)} to {str(copy_latest_checkpoint)}."
            )

    @classmethod
    def get_execution_order(cls):
        eo = super().get_execution_order()
        eo["setup_experiment"].append("SaveFinalCheckPoint: Get path to copy into.")
        eo["stop_experiment"].append(
            "SaveFinalCheckPoint: Copy final checkpoint to specified directory."
        )
        return eo
