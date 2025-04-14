"""
NBA Player Stat Comparison Tool

This script reads performance statistics for NBA players from a CSV file and provides
a user-friendly interface to compare the statistics of two players. The comparison
is visualized using bar charts and pie charts, allowing for a comprehensive look at
various performance metrics such as points, assists, rebounds, and shooting percentages.

Requirements: pandas, matplotlib, seaborn, numpy

Usage: Run the script, input the names of two players when prompted,
and view the generated comparison charts.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# create folder
output_folder = "plots"
os.makedirs(output_folder, exist_ok=True)


# initialize filename
FILENAME = "NBA_stat_2023_2024.csv"
## Read the CSV file containing NBA player statistics and specify \
# the encoding to handle any special characters.
df = pd.read_csv(FILENAME, encoding="latin-1")
# print the first 5 row of the dataset
# print(df.head())

# Select the relevant columns for analysis
# Keeping only the necessary columns: Player name, Points, Assists,
# 3-Point Percentage, Field Goal Percentage, Rebounds, Steals, Blocks,Turnovers
df = df[["Player", "PTS", "AST", "3P%", "FG%", "TRB", "STL", "BLK", "TOV"]]
df2 = df[["Player", "PTS", "AST"]].copy()
df3 = df[["Player", "TRB", "TOV"]].copy()
df4 = df[["Player", "STL", "BLK"]].copy()
df5 = df[["Player", "3P%", "FG%"]].copy()
# Remove rows with NaN values to ensure complete data for analysis
df.dropna(inplace=True)
# make the player names in lower columns
df2["Player"] = df2["Player"].str.lower()
df3["Player"] = df3["Player"].str.lower()
df4["Player"] = df4["Player"].str.lower()
df5["Player"] = df5["Player"].str.lower()
# set player as index
df2.set_index("Player", inplace=True)
df3.set_index("Player", inplace=True)
df4.set_index("Player", inplace=True)
df5.set_index("Player", inplace=True)


def player_prompt():
    """Prompt the user to input the names of two players for comparison.

    Returns:
        tuple: A tuple containing the lowercased names of the two players if valid."""

    print(" 📊 NBA Player Stat Comparison Tool for The 2023/2024 Season")

    while True:
        player1 = input("Enter the name of the first player: ").lower().strip()
        player2 = input("Enter the name of the second player: ").lower().strip()

        if player1 == player2:
            print("⚠️ You cannot compare the same basketballer. Try again.\n")
            continue

        if (
            player1 in df2.index
            and player2 in df2.index
            and player1 in df3.index
            and player2 in df3.index
            and player1 in df4.index
            and player2 in df4.index
            and player1 in df5.index
            and player2 in df5.index
        ):
            print(f"\nYou want to compare {player1.title()} to {player2.title()}")
            print("Please be patient...\n")
            return player1, player2
        else:
            print(
                "❌ One or both player names are incorrect or not in the dataset. Try again.\n"
            )


def plot_stat_comparison_chart(player1, player2):
    # Extract the statistics for a player from the DataFrame
    stats_of_player1 = df2.loc[player1]
    stats_of_player2 = df2.loc[player2]
    efficiency_stats_of_player1 = df3.loc[player1]
    efficiency_stats_of_player2 = df3.loc[player2]
    defensive_stats_of_player1 = df4.loc[player1]
    defensive_stats_of_player2 = df4.loc[player2]
    shooting_efficiency_of_player1 = df5.loc[player1]
    shooting_efficiency_of_player2 = df5.loc[player2]
    # labels we would be plotting on the x axis
    labels = ["PTS", "AST"]
    labels1 = ["TRB", "TOV"]
    labels2 = ["STL", "BLK"]
    labels3 = ["3P%", "FG%"]
    # extracts the values of the stats of the labels
    player1_stats = stats_of_player1[labels].values
    player2_stats = stats_of_player2[labels].values
    player1_efficiency_stats = efficiency_stats_of_player1[labels1].values
    player2_eficiency_stats = efficiency_stats_of_player2[labels1].values
    player1_defensive_stats = defensive_stats_of_player1[labels2].values
    player2_defensive_stats = defensive_stats_of_player2[labels2].values
    player1_shooting_efficiency_stats = shooting_efficiency_of_player1[labels3].values
    player2_shooting_efficiency_stats = shooting_efficiency_of_player2[labels3].values

    comparison_df = pd.DataFrame(
        {
            "stats": labels * 2,
            "values": np.concatenate([player1_stats, player2_stats]),
            "player": [player1] * len(labels) + [player2] * len(labels),
        }
    )
    # 2nd data frame
    efficiency_comparison_df = pd.DataFrame(
        {
            "stats": labels1 * 2,
            "values": np.concatenate(
                [player1_efficiency_stats, player2_eficiency_stats]
            ),
            "player": [player1] * len(labels) + [player2] * len(labels),
        }
    )

    # 3rd data frame
    defensive_stats_comparison_df = pd.DataFrame(
        {
            "stats": labels2 * 2,
            "values": np.concatenate(
                [player1_defensive_stats, player2_defensive_stats]
            ),
            "player": [player1] * len(labels) + [player2] * len(labels),
        }
    )
    # 4th data frame
    shooting_efficiency_comparison_df = pd.DataFrame(
        {
            "stats": labels3 * 2,
            "values": np.concatenate(
                [player1_shooting_efficiency_stats, player2_shooting_efficiency_stats]
            ),
            "player": [player1] * len(labels) + [player2] * len(labels),
        }
    )

    # figure of width 10 and height 6
    fig, ax = plt.subplots(2, 2, figsize=(10, 6))
    # Create a bar plot for comparing points and assists between the two players
    sns.barplot(
        data=comparison_df,
        x="stats",
        y="values",
        hue="player",
        ax=ax[0, 0],
        palette="icefire",
    )
    # adding labels
    ax[0, 0].set_xlabel("Stat Categories", fontfamily="DejaVu Serif")
    ax[0, 0].set_ylabel("Values", fontfamily="DejaVu Serif")
    ax[0, 0].set_title(
        f"{player1.title()} vs {player2.title()} \n (Points vs Assists)",
        fontfamily="DejaVu Serif",
    )
    ax[0, 0].legend()
    ax[0, 0].grid(
        axis="y",
        linestyle="--",
        alpha=0.6,
    )
    # create a bar plot for comparing Total Rebounds and Turnovers between the two players
    sns.barplot(
        data=efficiency_comparison_df,
        x="stats",
        y="values",
        hue="player",
        ax=ax[0, 1],
        palette="cubehelix",
    )

    # adding labels
    ax[0, 1].set_xlabel("Stat Categories", fontfamily="DejaVu Serif")
    ax[0, 1].set_ylabel("Values", fontfamily="DejaVu Serif")
    ax[0, 1].set_title(
        f"{player1.title()} vs {player2.title()} \n (Total Rebounds vs Turnovers)",
        fontfamily="DejaVu Serif",
    )

    ax[0, 1].legend()
    ax[0, 1].grid(
        axis="y",
        linestyle="--",
        alpha=0.6,
    )

    # create a bar plot for comparing Steals and Blocks between the two players
    sns.barplot(
        data=defensive_stats_comparison_df,
        x="stats",
        y="values",
        hue="player",
        ax=ax[1, 0],
    )
    # adding labels
    ax[1, 0].set_xlabel("Stat Categories", fontfamily="DejaVu Serif")
    ax[1, 0].set_ylabel("Values", fontfamily="DejaVu Serif")
    ax[1, 0].set_title(
        f"{player1.title()} vs {player2.title()} \n (Steals vs Blocks)",
        fontfamily="DejaVu Serif",
    )

    ax[1, 0].legend()
    ax[1, 0].grid(
        axis="y",
        linestyle="--",
        alpha=0.6,
    )
    # create a bar plot for comparing 3-Pointers and Field Goals between the two players

    sns.barplot(
        data=shooting_efficiency_comparison_df,
        x="stats",
        y="values",
        hue="player",
        ax=ax[1, 1],
        palette="rocket_r",
    )
    # adding labels
    ax[1, 1].set_xlabel("Stat Categories", fontfamily="DejaVu Serif")
    ax[1, 1].set_ylabel("Values", fontfamily="DejaVu Serif")
    # Title
    ax[1, 1].set_title(
        f"{player1.title()} vs {player2.title()}\n (3-Pointers vs Field Goals)",
        fontfamily="DejaVu Serif",
    )

    ax[1, 1].legend()
    ax[1, 1].grid(
        axis="y",
        linestyle="--",
        alpha=0.6,
    )

    # overall layout
    plt.suptitle("NBA 2023/2024 Season Stats", fontfamily="DejaVu Serif", fontsize=15)
    plt.tight_layout()


def save_fig(player1, player2):
    """Requests the user's answer to save the file according to a certain format."""
    print("\nWould you love to save this file?")
    save_fig_prompt = input("\nEnter yes or no to proceed: ").lower()
    if save_fig_prompt != "no":
        supported_formats = ["png", "pdf", "tiff", "jpg", "svg"]
        print(f"You can save the file in: {', '.join(supported_formats).upper()}")

        while True:
            file_format = (
                input("Enter the format you want to save the chart as: ")
                .lower()
                .strip()
            )

            if file_format in supported_formats:
                NAME_OF_FILE = (
                    f"{output_folder}/comparison_chart_of_{player1}_to_{player2}"
                )
                plt.savefig(
                    f"{NAME_OF_FILE}.{file_format}", format=file_format, dpi=300
                )
                print(f"\nChart saved successfully as {NAME_OF_FILE}.{file_format} 🎉")
                break
            else:
                print("❌ Invalid format. Please enter a valid format.")
    else:
        plt.show()

def clear_terminal():
    """Clears the terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    """Runs the NBA Stats Comparison Tool in a loop,
    allowing users to compare two players repeatedly."""

    while True:
        
        clear_terminal()
        player1, player2 = player_prompt()
        if player1 and player2:
            plot_stat_comparison_chart(player1, player2)
            save_fig(player1, player2)
            # show the file(optional)
            plt.show()
            print("\nDo you want to make another comparison? ")
            tool_prompt = input("Enter yes or no: ").strip().lower()
            if tool_prompt in ["yes", "y"]:
                #clear_terminal()
                continue
            elif tool_prompt in ["no", "n"]:
                print("👋 Exiting comparison tool.")
                break
            else:
                print("❌ Invalid input. Exiting.")
                break


if __name__ == "__main__":
    main()
