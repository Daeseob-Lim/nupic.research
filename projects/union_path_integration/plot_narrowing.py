# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2018, Numenta, Inc.  Unless you have an agreement
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

"""Plot location module representations during narrowing."""

import argparse
import json
import os

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

CWD = os.path.dirname(os.path.realpath(__file__))
CHART_DIR = os.path.join(CWD, "charts")


def examplesChart(
    inFilename, outFilename, objectCount, objectNumbers, moduleNumbers, scrambleCells
):
    if not os.path.exists(CHART_DIR):
        os.makedirs(CHART_DIR)

    with open(inFilename, "r") as f:
        experiments = json.load(f)
    for exp in experiments:
        numObjects = exp[0]["numObjects"]
        if numObjects == objectCount:
            locationLayerTimelineByObject = dict(
                (int(k), v) for k, v in exp[1]["locationLayerTimelineByObject"].items()
            )
            inferredStepByObject = dict(
                (int(k), v) for k, v in exp[1]["inferredStepByObject"].items()
            )
            break

    numSteps = 9
    numModules = 3
    numCells = 100
    numObjs = len(objectNumbers)
    width = 15

    cellSortOrder = np.arange(numCells)
    if scrambleCells:
        np.random.seed(42)
        np.random.shuffle(cellSortOrder)

    # Fit this number of objects to a single column of a sheet of paper
    defaultNumObjects = 3

    fig, axes = plt.subplots(
        numModules,
        numObjs,
        figsize=((3.25 / defaultNumObjects) * numObjs, 2.8),
        tight_layout={"pad": 0},
    )
    for i, obj in enumerate(objectNumbers):
        plotData = np.ones(
            (numCells * numModules, numSteps * width, 3), dtype=np.float32
        )
        for step, modules in enumerate(locationLayerTimelineByObject[obj]):
            if step >= numSteps:
                continue
            for moduleDisplayIndex, module in enumerate(moduleNumbers):
                cells = [
                    idx + (moduleDisplayIndex * numCells)
                    for idx in modules[module]["activeCells"]
                ]
                stepStart = step * width
                stepStop = (step + 1) * width
                plotData[cells, stepStart:stepStop, :] = [0, 0, 0]

        for m in range(numModules):
            if inferredStepByObject[obj] is not None:
                axes[m, i].add_patch(
                    matplotlib.patches.Rectangle(
                        ((inferredStepByObject[obj] - 1) * width, -1),
                        width,
                        numCells + 2,
                        color="red",
                        fill=False,
                    )
                )
            axes[m, i].set_yticks([])
            if m == numModules - 1:
                axes[m, i].set_xlabel("Object {}".format(i + 1), labelpad=5)
            if m == 0:
                axes[m, i].xaxis.tick_top()
                axes[m, i].xaxis.set_ticks_position("none")
                axes[m, i].xaxis.set_label_position("top")
                axes[m, i].tick_params(axis="x", which="major", pad=-2)
                axes[m, i].set_xticks(np.arange(10) * width + (width / 2))
                axes[m, i].set_xticklabels([str(v + 1) for v in np.arange(10)])
                axes[m, i].set_xlabel("Sensation")
            else:
                axes[m, i].set_xticks([])
            if i == 0:
                axes[m, i].set_ylabel("Module {}".format(m + 1))

            moduleData = plotData[m * numCells : (m + 1) * numCells]
            moduleData = moduleData[cellSortOrder]

            axes[m, i].imshow(moduleData, interpolation="none", aspect="auto")

    plt.subplots_adjust(wspace=3.0)
    filename = os.path.join(CHART_DIR, outFilename)
    print("Saving", filename)
    plt.savefig(filename)


def main():
    plt.rc("font", **{"family": "sans-serif", "sans-serif": ["Arial"], "size": 8})

    parser = argparse.ArgumentParser()
    parser.add_argument("--inFile", type=str, required=True)
    parser.add_argument("--outFile1", type=str, required=True)
    parser.add_argument("--outFile2", type=str, required=True)
    parser.add_argument("--exampleObjectCount", type=int, default=100)
    parser.add_argument("--exampleObjectNumbers", type=int, nargs="+", default=-1)
    parser.add_argument(
        "--exampleModuleNumbers", type=int, nargs="+", default=list(range(3))
    )
    parser.add_argument("--scrambleCells", action="store_true")
    args = parser.parse_args()

    exampleObjectNumbers = (
        args.exampleObjectNumbers
        if args.exampleObjectNumbers != -1
        else list(range(args.exampleObjectCount))
    )

    examplesChart(
        args.inFile,
        args.outFile1,
        args.exampleObjectCount,
        exampleObjectNumbers,
        args.exampleModuleNumbers,
        args.scrambleCells,
    )


if __name__ == "__main__":
    main()
