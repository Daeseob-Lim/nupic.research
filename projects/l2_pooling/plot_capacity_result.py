# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2016, Numenta, Inc.  Unless you have an agreement
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

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

from capacity_test import (
    DEFAULT_PLOT_DIR_NAME,
    DEFAULT_RESULT_DIR_NAME,
    _prepareResultsDir,
    plotResults,
)

plt.ion()


def main():
    numCorticalColumns = 1
    confusionThreshold = 30

    resultDirName = DEFAULT_RESULT_DIR_NAME
    plotDirName = DEFAULT_PLOT_DIR_NAME

    DEFAULT_COLORS = ("b", "r", "c", "g", "m")

    # Plot capacity vs L4 size
    expParams = []
    expParams.append(
        {"l4Column": 150, "externalInputSize": 2400, "w": 20, "sample": 6, "thresh": 3}
    )
    expParams.append(
        {"l4Column": 200, "externalInputSize": 2400, "w": 20, "sample": 6, "thresh": 3}
    )
    expParams.append(
        {"l4Column": 250, "externalInputSize": 2400, "w": 20, "sample": 6, "thresh": 3}
    )

    # plot result
    ploti = 0
    fig, ax = plt.subplots(2, 2)
    st = fig.suptitle(
        "Varying number of objects ({} cortical column{})".format(
            numCorticalColumns, "s" if numCorticalColumns > 1 else ""
        ),
        fontsize="x-large",
    )

    for axi in (0, 1):
        for axj in (0, 1):
            ax[axi][axj].xaxis.set_major_locator(ticker.MultipleLocator(100))

    legendEntries = []
    for expParam in expParams:
        expname = "multiple_column_capacity_varying_object_num_synapses_{}_thresh_{}_l4column_{}".format(  # noqa
            expParam["sample"], expParam["thresh"], expParam["l4Column"]
        )

        resultFileName = _prepareResultsDir(
            "{}.csv".format(expname), resultDirName=resultDirName
        )

        result = pd.read_csv(resultFileName)

        plotResults(
            result, ax, "numObjects", None, DEFAULT_COLORS[ploti], confusionThreshold, 0
        )
        ploti += 1
        legendEntries.append(
            "L4 mcs {} w {} s {} thresh {}".format(
                expParam["l4Column"],
                expParam["w"],
                expParam["sample"],
                expParam["thresh"],
            )
        )
    ax[0, 0].legend(legendEntries, loc=4, fontsize=8)
    fig.tight_layout()

    # shift subplots down:
    st.set_y(0.95)
    fig.subplots_adjust(top=0.85)

    plt.savefig(
        os.path.join(plotDirName, "capacity_varying_object_num_l4size_summary.pdf")
    )

    # Plot capacity vs L2 size

    expParams = []
    expParams.append(
        {
            "L2cellCount": 2048,
            "L2activeBits": 40,
            "w": 10,
            "sample": 6,
            "thresh": 3,
            "l2Column": 1,
        }
    )
    expParams.append(
        {
            "L2cellCount": 4096,
            "L2activeBits": 40,
            "w": 10,
            "sample": 6,
            "thresh": 3,
            "l2Column": 1,
        }
    )
    expParams.append(
        {
            "L2cellCount": 6144,
            "L2activeBits": 40,
            "w": 10,
            "sample": 6,
            "thresh": 3,
            "l2Column": 1,
        }
    )

    # plot result
    ploti = 0
    fig, ax = plt.subplots(2, 2)
    st = fig.suptitle("Varying number of objects", fontsize="x-large")

    for axi in (0, 1):
        for axj in (0, 1):
            ax[axi][axj].xaxis.set_major_locator(ticker.MultipleLocator(100))

    legendEntries = []
    for expParam in expParams:
        expName = "multiple_column_capacity_varying_object_num_synapses_{}_thresh_{}_l2Cells_{}_l2column_{}".format(  # noqa
            expParam["sample"],
            expParam["thresh"],
            expParam["L2cellCount"],
            expParam["l2Column"],
        )

        resultFileName = _prepareResultsDir(
            "{}.csv".format(expName), resultDirName=resultDirName
        )

        result = pd.read_csv(resultFileName)

        plotResults(
            result, ax, "numObjects", None, DEFAULT_COLORS[ploti], confusionThreshold, 0
        )
        ploti += 1
        legendEntries.append(
            "L2 cells {}/{} #cc {} ".format(
                expParam["L2activeBits"], expParam["L2cellCount"], expParam["l2Column"]
            )
        )
    ax[0, 0].legend(legendEntries, loc=3, fontsize=8)
    fig.tight_layout()

    # shift subplots down:
    st.set_y(0.95)
    fig.subplots_adjust(top=0.85)

    plt.savefig(os.path.join(plotDirName, "capacity_vs_L2size.pdf"))

    # Plot capacity vs number of cortical columns

    expParams = []
    expParams.append(
        {
            "l4Column": 150,
            "externalInputSize": 2400,
            "w": 10,
            "sample": 6,
            "thresh": 3,
            "l2Column": 1,
        }
    )
    expParams.append(
        {
            "l4Column": 150,
            "externalInputSize": 2400,
            "w": 10,
            "sample": 6,
            "thresh": 3,
            "l2Column": 2,
        }
    )
    expParams.append(
        {
            "l4Column": 150,
            "externalInputSize": 2400,
            "w": 10,
            "sample": 6,
            "thresh": 3,
            "l2Column": 3,
        }
    )

    # plot result
    ploti = 0
    fig, ax = plt.subplots(2, 2)
    st = fig.suptitle("Varying number of columns", fontsize="x-large")

    for axi in (0, 1):
        for axj in (0, 1):
            ax[axi][axj].xaxis.set_major_locator(ticker.MultipleLocator(100))

    legendEntries = []
    for expParam in expParams:
        expName = "multiple_column_capacity_varying_object_num_synapses_{}_thresh_{}_l4column_{}_l2column_{}".format(  # noqa
            expParam["sample"],
            expParam["thresh"],
            expParam["l4Column"],
            expParam["l2Column"],
        )

        resultFileName = _prepareResultsDir(
            "{}.csv".format(expName), resultDirName=resultDirName
        )

        result = pd.read_csv(resultFileName)

        plotResults(
            result, ax, "numObjects", None, DEFAULT_COLORS[ploti], confusionThreshold, 0
        )
        ploti += 1
        legendEntries.append(
            "L4 mcs {} #cc {} ".format(expParam["l4Column"], expParam["l2Column"])
        )

    ax[0, 0].legend(legendEntries, loc=3, fontsize=8)
    # shift subplots down:
    st.set_y(0.95)
    fig.subplots_adjust(top=0.85)

    plt.savefig(os.path.join(plotDirName, "capacity_vs_num_columns.pdf"))


if __name__ == "__main__":
    main()
