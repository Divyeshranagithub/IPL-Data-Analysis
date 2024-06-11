import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('df.csv')
matches = pd.read_csv('matches (1).csv')
top_batsman = pd.read_csv('top_10_batsman.csv')
top_bowler = pd.read_csv('top_10_bowler.csv')
top_10_teams = pd.read_csv('top_10_teams.csv')
top_bowler.rename(columns={'No_Of_Wickets':'Total_Wickets'}, inplace=True)

df['year'] = df['year'].astype(str)

def team_analysis(year, team):
    if team != 'All' and year != 'All':
        if df[df['year'] == year]['team1'].isin([team]).sum() > 0:
            y_df = pd.DataFrame(df[(df['year'] == year) & ((df['team1'] == team) | (df['team2'] == team))]).reset_index(
                drop=True)
            st.subheader(f'Overall Analysis of {team} in {year}')
            st.write(f'Total Matches Played By {team}:', y_df.shape[0])
            st.table(y_df)
            IPL_winner = y_df['winner'].iloc[-1]
            st.success(f'IPL trophy winners in {year} : "{IPL_winner}"', icon="🏆")
        else:
            st.warning(f':red[No data available for year {year} of team {team}]', icon="⚠️")
            return None
        return None
    elif team != 'All' and year == 'All':
        y_df = pd.DataFrame(df[(df['team1'] == team) | (df['team2'] == team)]).reset_index(drop=True)
        st.subheader(f'Overall Analysis of {team}')
        st.write('Total Matches Played:', y_df.shape[0])
        st.dataframe(y_df)
        # st.write(f'IPL trophy winners of {year} : "', y_df['winner'].iloc[-1], '"')
        return None
    elif team == 'All' and year != 'All':
        y_df = pd.DataFrame(df[df['year'] == year]).reset_index(drop=True)
        st.subheader(f'Overall Analysis of {year}')
        st.write('Total Matches Played:', y_df.shape[0])
        st.dataframe(y_df)
        IPL_winner = y_df['winner'].iloc[-1]
        st.success(f'IPL trophy winners in {year} : "{IPL_winner}"', icon="🏆")
        return None
    else:
        st.subheader('Overall IPL Matches from 2008-2023')
        st.write('Total Matches Played:', df.shape[0])
        st.dataframe(df)
        # st.write(f'IPL trophy winners of {year} : "', df['winner'].iloc[-1], '"')
        return None


def particapation(df):
    l1 = []
    for i in df['year'].value_counts().index.sort_values():
        l1.append(df[df['year'] == i]['team1'].unique().shape[0])
    fig = px.line(x=df['year'].value_counts().index.sort_values(), y=l1)

    fig.update_layout(title='Participation of Teams in IPL from 2008-2023', xaxis_title='Year',
                      yaxis_title='No of Teams')
    with st.container(border=True):
        st.plotly_chart(fig)
    return None


def matches_on_venue(df):
    l1 = []
    l2 = []
    for i in df['venue'].value_counts().index:
        l1.append(i)
        l2.append((df[df['venue'] == i].value_counts().sum()))
    t_df = pd.DataFrame(l1, columns=['venue'])
    t_df['no_of_matches'] = l2
    t_df.sort_values('venue', ascending=False)

    fig = px.bar(x=t_df['venue'], y=t_df['no_of_matches'])
    fig.update_layout(title='Matches Played on Venues from 2008-2023', xaxis_title='Venue', yaxis_title='No of Matches')
    with st.container(border=True):
        st.plotly_chart(fig)
    return None


def Team_decision_score():
    fig = px.bar(x=top_10_teams['Team_Name'], y=top_10_teams['TossWin_MatchWin'], color=top_10_teams['Team_Name'])
    fig.update_layout(title='Team TossWin-MatchWin Score', xaxis_title='Team Name', yaxis_title='Score')
    with st.container(border=True):
        st.plotly_chart(fig)
    return None

def winnerteam(df):
    colors = ['yellow', 'blue', 'purple', 'pink', 'silver', 'orange', 'darkblue']
    fig = px.bar(x=df[df['match_type'] == 'Final']['winner'].value_counts().index,
                 y=df[df['match_type'] == 'Final']['winner'].value_counts(),
                 color=df[df['match_type'] == 'Final']['winner'].value_counts().index, color_discrete_sequence=colors)
    fig.update_layout(title='IPL Trophy Winners from 2008-2023', xaxis_title='Teams', yaxis_title='No of Trophies')
    with st.container(border=True):
        st.plotly_chart(fig)
    return None


def team_compared(team1, team2):
    total_win_t1 = df[(df['team1'] == team1) & (df['team2'] == team2) & (df['winner'] == team1)].value_counts().sum() + \
                   df[(df['team1'] == team2) & (df['team2'] == team1) & (df['winner'] == team1)].value_counts().sum()
    total_win_t2 = df[(df['team1'] == team1) & (df['team2'] == team2) & (df['winner'] == team2)].value_counts().sum() + \
                   df[(df['team1'] == team1) & (df['team2'] == team1) & (df['winner'] == team2)].value_counts().sum()
    total_match = total_win_t1 + total_win_t2
    return total_match, total_win_t1, total_win_t2


def team_run_compared(team1, team2):
    t1 = []
    t2 = []
    for i in matches['year'].unique():
        t1.append(matches[((matches['team1'] == team1) | (matches['team2'] == team1)) & (
            matches['toss_winner'] != team1) & (matches['toss_decision'] == 'field') & (
                              matches['year'] == i)]['target_runs'].sum() + matches[
                      (matches['toss_winner'] == team1) & (matches['toss_decision'] == 'bat') & (
                          matches['year'] == i)]['target_runs'].sum())
        t2.append(matches[
                      ((matches['team1'] == team2) | (matches['team2'] == team2)) & (
                          matches['toss_winner'] != team2) & (
                          matches['toss_decision'] == 'field') & (matches['year'] == i)]['target_runs'].sum() +
                  matches[(matches['toss_winner'] == team2) & (matches['toss_decision'] == 'bat') & (
                      matches['year'] == i)]['target_runs'].sum())
    t_df = pd.DataFrame(t1, columns=[team1])
    t_df[team2] = t2
    fig = px.line(t_df, x=matches['year'].unique(), y=[team1, team2])
    fig.update_layout(title='Compared Team by Runs', xaxis_title='Year', yaxis_title='Runs')
    st.plotly_chart(fig)
    return None


def top_10_batsman():
    st.subheader('Top 10 Batsman of IPL')
    st.table(top_batsman.sort_values('Total_Runs', ascending=False))

    with st.container(border=True):
        fig = px.bar(x=top_batsman['Player_Name'], y=top_batsman['Total_Runs'],
                     color=top_batsman['Player_Name'])
        fig.update_layout(title='Top 10 Batsman with Most Runs', xaxis_title='Player Name', yaxis_title='No of Awards')
        st.plotly_chart(fig)
    return None


def top_10_bowler():
    st.subheader('Top 10 Bowler of IPL')
    st.table(top_bowler.sort_values('No_Of_Awards', ascending=False))

    with st.container(border=True):
        fig = px.bar(x=top_bowler['Player_Name'], y=top_bowler['Total_Wickets'],
                     color=top_bowler['Player_Name'])
        fig.update_layout(title='Top 10 Bowler with Most Wickets', xaxis_title='Player Name', yaxis_title='No of Awards')
        st.plotly_chart(fig)
    return None
